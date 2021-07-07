import os
from pyrogram import Client

TRIGGERS = os.environ.get("TRIGGERS", "/ !").split()
API_HASH = os.environ.get("API_HASH")
BOT_TOKEN = os.environ.get("BOT_TOKEN")
BOT_NAME = os.environ.get("BOT_NAME")
DB_URL = os.environ.get("DATABASE_URL")
ANILIST_CLIENT = os.environ.get("ANILIST_CLIENT")
ANILIST_SECRET = os.environ.get("ANILIST_SECRET")
ANILIST_REDIRECT_URL = os.environ.get("ANILIST_REDIRECT_URL", "https://anilist.co/api/v2/oauth/pin")
API_ID = int(os.environ.get("API_ID"))
LOG_CHANNEL_ID = int(os.environ.get("LOG_CHANNEL_ID"))
OWNER = list(filter(lambda x: x, map(int, os.environ.get("OWNER_ID", "1005170481 972029825").split())))  ## sudos can be included

DOWN_PATH = "anibot/downloads/"
HELP_DICT = dict()

plugins = dict(root="anibot/plugins")
anibot = Client("anibot", bot_token=BOT_TOKEN, api_id=API_ID, api_hash=API_HASH, plugins=plugins)

HELP_DICT['杂项'] = '''
用于群组的指令：

/settings - 切换设置，比如是否允许R18，或者是否通知播出的动画。

/disable - 禁止群组内使用指令（通过在用户和用户之间添加空格来禁止多个用户使用指令）。
`/disable anime anilist 用户ID`

/enable - 允许群组内使用指令（通过在用户和用户之间添加空格来允许多个用户使用指令）。
`/enable anime anilist 用户ID`

/disabled - 列出被禁用使用指令的用户ID
'''

HELP_DICT["其他"] = """使用 /reverse 指令，通过 tracemoepy API 反向搜索来源
__注意：这在未经裁剪的动漫图片上效果最好。
当用于裁剪过的媒体时，你可能会得到结果，但可能不太可靠。__

使用 /schedule 指令来获取根据星期显示时间表

使用 /watch 指令来获得搜索到的动画的观看顺序

Use /fillers Command to get a list of fillers for an anime
"""

HELP_DICT["Anilist"] = """
下面是获取关于动漫、人物、漫画等信息的基本Anilist指令列表。

/anime - 使用此指令，使用关键词（动漫名称）或Anilist ID获得特定动漫的信息。
(可以查询续集和前传的信息)

/anilist - 使用此指令可在与搜索查询相关的多个相似的动画。
(不可以查询续集和前传的信息)

/character - 使用此指令来获取角色的信息

/manga - 使用这个指令来获取漫画的信息

/airing - 使用此指令来获取动画的播放状态

/top - 使用此指令查询某一类型/标签的排行或所有的动画。
(要获得可用的标签或类型的列表，请发送 /gettags 或 /getgenres )

/user - 使用此指令来获取一个匿名用户的信息
"""

HELP_DICT["高级"] = """
这包括高级的anilist功能

使用 /auth 或 !auth 指令 以获得关于如何用机器人授权你的Anilist账户的帮助
授权自己可以解锁机器人的高级功能，如:
- 将动漫/角色/漫画加入收藏夹
- 在你的搜索中查看你与动漫相关的数据，包括分数、状态和收藏。
- 解锁/flex 、/me 、/activity 和 /favourites 指令
- 添加/更新已完成或计划观看/阅读等清单条目
- 删除 anilist 条目

使用 /flex 或 !flex 指令获取Anilist统计信息

使用 /logout 或 !logout 指令解除绑定你的Anilist账户的

使用 /me 或 !me 指令获得你最近的活动信息
也可以使用 /activity 或 !activity

使用 /favourites 或 !favourites 指令获取你的anilist收藏夹
"""