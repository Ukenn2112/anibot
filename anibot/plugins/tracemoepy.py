# The following code is exact (almost i mean) copy of 
# reverse search taken from @DeletedUser420's Userge-Plugins repo
# originally authored by
# Phyco-Ninja (https://github.com/Phyco-Ninja) (@PhycoNinja13b)
# but is in current state after DeletedUser420's edits
# which made this code shorter and more efficient

import random
import asyncio
import tracemoepy
from tracemoepy.errors import ServerError
from aiohttp import ClientSession
from pyrogram import Client, filters
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup, CallbackQuery, InputMediaPhoto, InputMediaVideo, Message
from .. import BOT_NAME, TRIGGERS as trg
from ..utils.helper import check_user, control_user, media_to_image, rand_key
from ..utils.data_parser import check_if_adult
from ..utils.db import get_collection
from .anilist import no_pic

SFW_GRPS = get_collection("SFW_GROUPS")
DC = get_collection('DISABLED_CMDS')

TRACE_MOE = {}

@Client.on_message(filters.command(["reverse", f"reverse{BOT_NAME}"], prefixes=trg))
@control_user
async def trace_bek(client: Client, message: Message):
    """ 反向搜索动画段/图片 """
    gid = message.chat.id
    find_gc = await DC.find_one({'_id': gid})
    if find_gc is not None and 'reverse' in find_gc['cmd_list'].split():
        return
    x = await message.reply_text("正在反向搜索指定的媒体...")
    replied = message.reply_to_message
    if not replied:
        await x.edit_text("正在返回结果 !")
        await asyncio.sleep(5)
        await x.delete()
        return
    dls_loc = await media_to_image(client, message, x, replied)
    if dls_loc:
        async with ClientSession() as session:
            tracemoe = tracemoepy.AsyncTrace(session=session)
            try:
                search = await tracemoe.search(dls_loc, upload_file=True)
            except ServerError:
                await x.edit_text('服务器错误，正在重试')
                try:
                    search = await tracemoe.search(dls_loc, upload_file=True)
                except ServerError:
                    await x.edit_text('无法解析结果!!!')
                    return
            result = search["result"][0]
            caption_ = (
                f"**标题**: {result['anilist']['title']['native']} (`{result['anilist']['title']['english']}`)\n"
                f"\n**Anilist ID:** `{result['anilist']['id']}`"
                f"\n**相似度**: `{(str(result['similarity']*100))[:5]}`"
                f"\n**集数**: `{result['episode']}`"
            )
            preview = result['video']
        button = []
        nsfw = False
        if await check_if_adult(int(result['anilist']['id']))=="True" and await (SFW_GRPS.find_one({"id": gid})):
            msg = no_pic[random.randint(0, 4)]
            caption="所解析的结果似乎是R18，不允许在这个群组中出现。如果需要请私信我"
            nsfw = True
        else:
            msg = preview
            caption=caption_
            button.append([InlineKeyboardButton("更多信息", url=f"https://anilist.co/anime/{result['anilist']['id']}")])
        dls_js = rand_key()
        TRACE_MOE[dls_js] = dls_loc
        button.append([InlineKeyboardButton("下一个结果", callback_data=f"tracech_1_{dls_js}_{message.from_user.id}")])
        await (message.reply_video if nsfw is False else message.reply_photo)(msg, caption=caption, reply_markup=InlineKeyboardMarkup(button))
    else:
        await message.reply_text("无法解析结果!!!")
    await x.delete()


@Client.on_callback_query(filters.regex(pattern=r"tracech_(.*)"))
@check_user
async def tracemoe_btn(client: Client, cq: CallbackQuery):
    kek, page, dls_loc, user = cq.data.split("_")
    try:
        TRACE_MOE[dls_loc]
    except KeyError:
        return await cq.answer("查询已过期!!!\n请重新查询", show_alert=True)
    async with ClientSession() as session:
        tracemoe = tracemoepy.AsyncTrace(session=session)
        try:
            search = await tracemoe.search(TRACE_MOE[dls_loc], upload_file=True)
        except ServerError:
            return await cq.answer("服务器错误!!!\n请过一段时间后再试", show_alert=True)
        result = search["result"][int(page)]
        caption = (
            f"**更多信息**: {result['anilist']['title']['native']} (`{result['anilist']['title']['english']}`)\n"
            f"\n**Anilist ID:** `{result['anilist']['id']}`"
            f"\n**相似度**: `{(str(result['similarity']*100))[:5]}`"
            f"\n**集数**: `{result['episode']}`"
        )
        preview = result['video']
    button = []
    if await check_if_adult(int(result['anilist']['id']))=="True" and await (SFW_GRPS.find_one({"id": cq.message.chat.id})):
        msg = InputMediaPhoto(no_pic[random.randint(0, 4)], caption="所解析的结果似乎是R18，不允许在这个群组中出现。如果需要请私信我")
    else:
        msg = InputMediaVideo(preview, caption=caption)
        button.append([InlineKeyboardButton("更多信息", url=f"https://anilist.co/anime/{result['anilist']['id']}")])
    if int(page)==0:
        button.append([InlineKeyboardButton("下个结果", callback_data=f"tracech_{int(page)+1}_{dls_loc}_{user}")])
    elif int(page)==(len(search['result'])-1):
        button.append([InlineKeyboardButton("返回上个结果", callback_data=f"tracech_{int(page)-1}_{dls_loc}_{user}")])
    else:
        button.append([
            InlineKeyboardButton("返回上个结果", callback_data=f"tracech_{int(page)-1}_{dls_loc}_{user}"),
            InlineKeyboardButton("下个结果", callback_data=f"tracech_{int(page)+1}_{dls_loc}_{user}")
        ])
    await cq.edit_message_media(msg, reply_markup=InlineKeyboardMarkup(button))