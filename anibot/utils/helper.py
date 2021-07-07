import requests
import asyncio
import os
import shlex
from time import time
from datetime import datetime
from os.path import basename
from typing import Tuple, Optional
from uuid import uuid4
from pyrogram import Client
from pyrogram.errors import FloodWait, MessageNotModified
from pyrogram.types import InlineKeyboardButton, CallbackQuery, Message, InlineKeyboardMarkup
from .. import OWNER, DOWN_PATH, anibot, LOG_CHANNEL_ID
from ..utils.db import get_collection

AUTH_USERS = get_collection("AUTH_USERS")
IGNORE = get_collection("IGNORED_USERS")
USER_JSON = {}
USER_WC = {}


###### credits to @deleteduser420 on tg, code from USERGE-X ######


def rand_key():
    return str(uuid4())[:8]


def control_user(func):
    async def wrapper(_, msg: Message):
        user = msg.from_user.id
        if await IGNORE.find_one({'_id': user}):
            return
        nut = time()
        if user not in OWNER:
            try:
                out = USER_JSON[user]
                if nut-out<1.2:
                    USER_WC[user] += 1
                    if USER_WC[user] == 3:
                        await msg.reply_text(
                            "Stop spamming bot!!!\nElse you will be blacklisted",
                        )
                    if USER_WC[user] == 5:
                        await IGNORE.insert_one({'_id': user})
                        await msg.reply_text('You have been exempted from using this bot now due to spamming 5 times consecutively!!!\nTo remove restriction plead to @hanabi_support')
                        await clog('ANIBOT', f'UserID: {user}', 'BAN')
                        return
                    await asyncio.sleep(USER_WC[user])
                else:
                    USER_WC[user] = 0
            except KeyError:
                pass
            USER_JSON[user] = nut
        try:
            await func(_, msg)
        except FloodWait as e:
            await asyncio.sleep(e.x + 5)
        except MessageNotModified:
            pass
    return wrapper


def check_user(func):
    async def wrapper(_, c_q: CallbackQuery):
        user = c_q.from_user.id
        if await IGNORE.find_one({'_id': user}):
            return
        if user in OWNER or user==int(c_q.data.split("_").pop()):
            if user not in OWNER:
                nt = time()
                try:
                    ot = USER_JSON[user]
                    if nt-ot<1.4:
                        await c_q.answer(
                            "Stop spamming bot!!!\nElse you will be blacklisted",
                        )
                        await clog('ANIBOT', f'UserID: {user}', 'SPAM')
                except KeyError:
                    pass
                USER_JSON[user] = nt
            try:
                await func(_, c_q)
            except FloodWait as e:
                await asyncio.sleep(e.x + 5)
            except MessageNotModified:
                pass
        else:
            await c_q.answer(
                "Not your query!!!",
                show_alert=True,
            )
    return wrapper


async def media_to_image(client: Client, message: Message, x: Message, replied: Message):
    if not (
        replied.photo
        or replied.sticker
        or replied.animation
        or replied.video
    ):
        await x.edit_text("Media Type Is Invalid !")
        await asyncio.sleep(5)
        await x.delete()
        return
    media = replied.photo or replied.sticker or replied.animation or replied.video
    if not os.path.isdir(DOWN_PATH):
        os.makedirs(DOWN_PATH)
    dls = await client.download_media(
        media,
        file_name=DOWN_PATH + rand_key(),
    )
    dls_loc = os.path.join(DOWN_PATH, os.path.basename(dls))
    if replied.sticker and replied.sticker.file_name.endswith(".tgs"):
        png_file = os.path.join(DOWN_PATH, f"{rand_key()}.png")
        cmd = f"lottie_convert.py --frame 0 -if lottie -of png {dls_loc} {png_file}"
        stdout, stderr = (await runcmd(cmd))[:2]
        os.remove(dls_loc)
        if not os.path.lexists(png_file):
            await x.edit_text("This sticker is Gey, Task Failed Successfully ≧ω≦")
            await asyncio.sleep(5)
            await x.delete()
            raise Exception(stdout + stderr)
        dls_loc = png_file
    elif replied.sticker and replied.sticker.file_name.endswith(".webp"):
        stkr_file = os.path.join(DOWN_PATH, f"{rand_key()}.png")
        os.rename(dls_loc, stkr_file)
        if not os.path.lexists(stkr_file):
            await x.edit_text("```Sticker not found...```")
            await asyncio.sleep(5)
            await x.delete()
            return
        dls_loc = stkr_file
    elif replied.animation or replied.video:
        await x.edit_text("`Converting Media To Image ...`")
        jpg_file = os.path.join(DOWN_PATH, f"{rand_key()}.jpg")
        await take_screen_shot(dls_loc, 0, jpg_file)
        os.remove(dls_loc)
        if not os.path.lexists(jpg_file):
            await x.edit_text("This Gif is Gey (｡ì _ í｡), Task Failed Successfully !")
            await asyncio.sleep(5)
            await x.delete()
            return
        dls_loc = jpg_file
    return dls_loc


async def runcmd(cmd: str) -> Tuple[str, str, int, int]:
    """ run command in terminal """
    args = shlex.split(cmd)
    process = await asyncio.create_subprocess_exec(
        *args, stdout=asyncio.subprocess.PIPE, stderr=asyncio.subprocess.PIPE
    )
    stdout, stderr = await process.communicate()
    return (
        stdout.decode("utf-8", "replace").strip(),
        stderr.decode("utf-8", "replace").strip(),
        process.returncode,
        process.pid,
    )


async def take_screen_shot(
    video_file: str, duration: int, path: str = ""
) -> Optional[str]:
    """ take a screenshot """
    print(
        "[[[Extracting a frame from %s ||| Video duration => %s]]]",
        video_file,
        duration,
    )
    ttl = duration // 2
    thumb_image_path = path or os.path.join(
        DOWN_PATH, f"{basename(video_file)}.jpg"
    )
    command = f'''ffmpeg -ss {ttl} -i "{video_file}" -vframes 1 "{thumb_image_path}"'''
    err = (await runcmd(command))[1]
    if err:
        print(err)
    return thumb_image_path if os.path.exists(thumb_image_path) else None


##################################################################


async def return_json_senpai(query: str, vars_: dict, auth: bool = False, user: int = None):
    if auth  is False:
        url = "https://graphql.anilist.co"
        response = requests.post(url, json={"query": query, "variables": vars_}).json()
    else:
        headers = {
        'Authorization': 'Bearer ' + str((await AUTH_USERS.find_one({"id": int(user)}))['token']),
        'Content-Type': 'application/json',
        'Accept': 'application/json',
        }
        url = "https://graphql.anilist.co"
        response = requests.post(url, json={"query": query, "variables": vars_}, headers=headers).json()
    return response


def cflag(country):
    if country == "JP":
        return "\U0001F1EF\U0001F1F5"
    if country == "CN":
        return "\U0001F1E8\U0001F1F3"
    if country == "KR":
        return "\U0001F1F0\U0001F1F7"
    if country == "TW":
        return "\U0001F1F9\U0001F1FC"


def pos_no(x):
    th = "st" if x == "1" else "nd" if x == "2" else "rd" if x == "3" else "th"
    return th


def ss(x: int):
    if x==1:
        return ""
    else:
        return "s"


def make_it_rw(time_stamp):
    """Converting Time Stamp to Readable Format"""
    seconds, milliseconds = divmod(int(time_stamp), 1000)
    minutes, seconds = divmod(seconds, 60)
    hours, minutes = divmod(minutes, 60)
    days, hours = divmod(hours, 24)
    tmp = (
        ((str(days) + " Days, ") if days else "")
        + ((str(hours) + " Hours, ") if hours else "")
        + ((str(minutes) + " Minutes, ") if minutes else "")
        + ((str(seconds) + " Seconds, ") if seconds else "")
        + ((str(milliseconds) + " ms, ") if milliseconds else "")
    )
    return tmp[:-2]


async def clog(name: str, text: str, tag: str):
    log = f"#{name.upper()}  #{tag.upper()}\n\n{text}"
    await anibot.send_message(chat_id=LOG_CHANNEL_ID, text=log)


def get_btns(media, user: int, result: list, lsqry: str = None, lspage: int = None, auth: bool = False, sfw: str = "False"):
    buttons = []
    qry = f"_{lsqry}" if lsqry  is not None else ""
    pg = f"_{lspage}" if lspage  is not None else ""
    if media == "ANIME" and sfw == "False":
        buttons.append([
            InlineKeyboardButton(text="角色", callback_data=f"char_{result[2][0]}_ANI{qry}{pg}_{str(auth)}_1_{user}"),
            InlineKeyboardButton(text="简介", callback_data=f"desc_{result[2][0]}_ANI{qry}{pg}_{str(auth)}_{user}"),
            InlineKeyboardButton(text="系列", callback_data=f"ls_{result[2][0]}_ANI{qry}{pg}_{str(auth)}_{user}"),
        ])
    if media == "CHARACTER":
        buttons.append([InlineKeyboardButton("Description", callback_data=f"desc_{result[2][0]}_CHAR{qry}{pg}_{str(auth)}_{user}")])
        buttons.append([InlineKeyboardButton("List Series", callback_data=f"lsc_{result[2][0]}{qry}{pg}_{str(auth)}_{user}")])
    if media == "SCHEDULED":
        if result[0]!=0 and result[0]!=6:
            buttons.append([
                InlineKeyboardButton(str(day_(result[0]-1)), callback_data=f"sched_{result[0]-1}_{user}"),
                InlineKeyboardButton(str(day_(result[0]+1)), callback_data=f"sched_{result[0]+1}_{user}")
            ])
        if result[0] == 0:
            buttons.append([InlineKeyboardButton(str(day_(result[0]+1)), callback_data=f"sched_{result[0]+1}_{user}")])
        if result[0] == 6:
            buttons.append([InlineKeyboardButton(str(day_(result[0]-1)), callback_data=f"sched_{result[0]-1}_{user}")])
    if media == "MANGA" and sfw == "False":
        buttons.append([InlineKeyboardButton("More Info", url=result[1][2])])
    if media == "AIRING" and sfw == "False":
        buttons.append([InlineKeyboardButton("More Info", url=result[1])])
    if auth is True and media!="SCHEDULED" and sfw == "False":
        auth_btns = get_auth_btns(media, user, result[2], lspage=lspage, lsqry=lsqry)
        buttons.append(auth_btns)
    if len(result)>3:
        if result[3] == "None":
            if result[4] != "None":
                buttons.append([InlineKeyboardButton(text="Sequel", callback_data=f"btn_{result[4]}_{str(auth)}_{user}")])
        else:
            if result[4] != "None":
                buttons.append([
                    InlineKeyboardButton(text="Prequel", callback_data=f"btn_{result[3]}_{str(auth)}_{user}"),
                    InlineKeyboardButton(text="Sequel", callback_data=f"btn_{result[4]}_{str(auth)}_{user}"),
                ])
            else:
                buttons.append([InlineKeyboardButton(text="Prequel", callback_data=f"btn_{result[3]}_{str(auth)}_{user}")])
    if lsqry  is not None and len(result)!=1 and result[1][1]!=1:
        if lspage == 1:
            buttons.append([InlineKeyboardButton(text="下一页", callback_data=f"page_{media}{qry}_{int(lspage)+1}_{str(auth)}_{user}")])
        elif lspage == result[1][1]:
            buttons.append([InlineKeyboardButton(text="上一页", callback_data=f"page_{media}{qry}_{int(lspage)-1}_{str(auth)}_{user}")])
        else:
            buttons.append([
                InlineKeyboardButton(text="上一页", callback_data=f"page_{media}{qry}_{int(lspage)-1}_{str(auth)}_{user}"),
                InlineKeyboardButton(text="下一页", callback_data=f"page_{media}{qry}_{int(lspage)+1}_{str(auth)}_{user}"),
            ])
    return InlineKeyboardMarkup(buttons)


def get_auth_btns(media, user, data, lsqry: str = None, lspage: int = None):
    btn = []
    qry = f"_{lsqry}" if lsqry  is not None else ""
    pg = f"_{lspage}" if lspage  is not None else ""
    if media=="CHARACTER":
        btn.append(InlineKeyboardButton(text="Add to Favs" if data[1] is not True else "Remove from Favs", callback_data=f"fav_{media}_{data[0]}{qry}{pg}_{user}"))
    else:
        btn.append(InlineKeyboardButton(text="Add to Favs" if data[3] is not True else "Remove from Favs", callback_data=f"fav_{media}_{data[0]}{qry}{pg}_{user}"))
        btn.append(InlineKeyboardButton(
            text="Add to List" if data[1] is False else "Update in List",
            callback_data=f"lsadd_{media}_{data[0]}{qry}{pg}_{user}" if data[1] is False else f"lsupdt_{media}_{data[0]}_{data[2]}{qry}{pg}_{user}"
            ))
    return btn


def day_(x: int):
    if x == 0: return "Monday"
    if x == 1: return "Tuesday"
    if x == 2: return "Wednesday"
    if x == 3: return "Thursday"
    if x == 4: return "Friday"
    if x == 5: return "Saturday"
    if x == 6: return "Sunday"


def season_(future: bool = False):
    k = datetime.now()
    m = k.month
    if future:
        m = m+3
    y = k.year
    if m > 12:
        y = y+1
    if m in [1, 2, 3] or m > 12:
        return 'WINTER', y
    if m in [4, 5, 6]:
        return 'SPRING', y
    if m in [7, 8, 9]:
        return 'SUMMER', y
    if m in [10, 11, 12]:
        return 'FALL', y