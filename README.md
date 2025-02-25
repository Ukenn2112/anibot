Telegram Bot Repo 能够通过 Anilist API 从 [AniFluid](https://t.me/anifluidbot) 和 [Nepgear](https://t.me/nepgearbot) 获取以下信息。
* 动漫
* 正在播放
* 漫画
* 角色
* 预定
* 最受欢迎的动画
* 最喜欢的作品
* 漫画家活动
* 使用机器人更新Anilist条目
* 流行的、趋势的和即将到来的某一季的动画
* 随机动画评分
* 动漫填充物来自[animefillerslist](https://www.animefillerlist.com)
* 使用[LiveChart](https://livechart.me)的动漫播放通知
* 动漫发布通知[Crunchyroll](https://crunchyroll.com)
* 动漫发布通知 [Subsplease](https://subsplease.org)
* 动漫反向搜索由[tracemoepy](https://github.com/dragsama/tracemoepy)提供
* 使用[web api](https://chiaki.vercel.app)从[Chiaki](https://chiaki.site/)观看指令。
<h3>还可以添加到群组并是否启用sfw锁，以防止成员查找hentai和R18的东西<br>使用指令禁用。</br></h3>

<img src='https://img.shields.io/github/repo-size/lostb053/anibot?style=flat-square'>  <img src='https://img.shields.io/github/license/lostb053/anibot?style=flat-square'>  <img src='https://img.shields.io/github/languages/top/lostb053/anibot?style=flat-square'>  [![CodeFactor](https://www.codefactor.io/repository/github/lostb053/anibot/badge)](https://www.codefactor.io/repository/github/lostb053/anibot)

## 环境要求
* Python 3.9.6
* Telegram [API Keys](https://my.telegram.org/apps)
* Bot Token from [BotFather](https://t.me/botfather)
* SauceNAO [API Keys](https://saucenao.com/)
* MongoDB [Database URL](https://cloud.mongodb.com/)
* Anilist [Client Keys](https://anilist.co/settings/developer)
* 为了使认证过程顺利进行，请部署[这个](https://github.com/lostb053/anilist_oauth_webserver)网络服务器 (一个无名的代码服务器，希望对你有帮助。)


## 可用指令
```
 /help - 获得关于机器人cmds的互动和详细帮助
 /ping - Ping机器人，检查它是否在线。
 /start - 在群组中启动机器人（将被记录）或在下午启动（如果不是所有者，用户将被记录）。
 /anime - 获取单部动画的信息(包括查找前传和续集的按钮)
 /anilist - 获取与查询有关的多部可能的动画的信息
 /character - 获取与查询有关的多个可能的人物信息
 /manga - 获取与查询相关的多种可能的漫画信息
 /airing - 获取动画的播出数据信息
 /flex - 获取授权用户的匿名信息
 /user - 获取与查询有关的名单信息
 /schedule - 获取动画播出时间表
 /auth - 获取关于如何授权动漫账户的信息
 /browse - 获取流行的、趋势的或即将播出的动画
 /quote - 获取随机报价
 /logout - 移除授权
 /settings - 在群组中切换nsfw锁定和播放通知
 /top - 检索某一类型或标签的顶级动画
 /reverse - 由tracemoepy驱动的反向搜索
 /watch - 检索动画系列的观看顺序
 /feedback - 联系机器人所有者或主要支持小组@hanabi_support
 /me 或 /activity - 获取 Anilist 最近的活动
 /fillers - 获取动画填充物的列表
 /disable - 禁用组中的一个指令
 /enable - 启用组内的一个指令
 /disabled - 在一个组中列出禁用的指令
 /favourites - 获得Anilist的最爱
 /gettags - 获取可用的标签列表
 /getgenres - 获取可用类型的列表
```


## 所有者指令
```
 /eval - 运行Python代码（代码必须在cmd之后开始，如"/eval print('UwU')"）。
 /term - 在终端运行代码
 /stats - 采集机器人的数据，如群组/用户数和PING数
 /dbcleanup - 清除数据库中无用的条目
```


## 一键部署
<p align="center"><a href="https://heroku.com/deploy?template=https://github.com/Ukenn2112/anibot"> <img src="https://img.shields.io/badge/Deploy%20To%20Heroku-blue?style=for-the-badge&logo=heroku" width="220" height="38.45"/></a></p>


## 引用
* AniList Api ([GitHub](https://github.com/AniList/ApiV2-GraphQL-Docs))
* jikanpy ([GitHub](https://github.com/abhinavk99/jikanpy))
* [@NotThatMF](https://t.me/notthatmf) for [chiaki fast api](https://chiaki.vercel.app/) and for creating base for this bot to work
* [@DragSama](https://t.me/dragsama) on telegram for [tracemoepy](https://github.com/dragsama/tracemoepy) & [AniFluid-Base](https://github.com/DragSama/AniFluid-Base)
* [@DeletedUser420](https://t.me/deleteduser420) on telegram for [USERGE-X](https://github.com/code-rgb/USERGE-X) & [Userge-Plugins](https://github.com/code-rgb/Userge-Plugins)
* [Phyco-Ninja](https://github.com/Phyco-Ninja) as author of anilist plugin in Userge-Plugins repo
* [@blank_x](https://t.me/blank_x) on tg for [sukuinote](https://gitlab.com/blank-x/sukuinote)


如需改进，请联系[@LostB053](https://t.me/lostb053) 或 [@hanabi_support](https://t.me/hanabi_support)<br>
也可以提要求支持，但不要期望太多（因为我自己还在学习）。<br>
<br>
<h4>注意：我放弃了SauceNAO，因为我不能以一种好看的方式来表示它。<br>
如果有人能帮助我解析结果并组织它们，如 <a href='https://t.me/reverseSearchBot'>@reverseSearchBot</a></h4>相似好看的，我将不胜感激。
