from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import require
from .config import Config

require("plugins.file_edit")
from plugins.file_edit import read_file, read_large_file, write_file, delete_file
require("plugins.agbi")
from plugins.agbi import c_coin, return_id

__plugin_meta__ = PluginMetadata(
    name="jiting_renshu",
    description="查机厅人数",
    usage="万几",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot.params import CommandArg
from nonebot.rule import to_me, startswith
from nonebot.plugin import on_command,on_message,on_regex
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters.qq import Message, MessageSegment
#from nonebot.adapters.console import Message, MessageEvent
from nonebot.adapters import Event
from nonebot.log import logger

import time
import random as rand

jt_report = on_command("jt")

@jt_report.handle()
async def _(event: Event, message: Message = CommandArg()):
    user_id = event.get_user_id()
    """try:
        user_id = event.get_user_id()
        platform = "QQ"
    except:
        user_id = "ConsoleUser"
        platform = "控制台" """
    user = await return_id(str(user_id))
    try:
        num = int(str(message).strip())
        if (num < 0) or num > 30:
            raise
    except Exception:
        await jt_report.finish(f"你觉得机厅人数可以是{str(message)}吗")
    text = f"{str(time.time())}\n{str(event.get_user_id())}\n{str(num)}"
    write_file("jiting.txt",text)
    val = rand.randint(2,5)
    c_coin(user_id,val)
    msg = f"{user}已更新人数为{str(num)}"
    await jt_report.finish(msg)

tj = on_regex(r".*万.*几.*")

@tj.handle()
async def _():
    try:
        tar=str(read_file("jiting.txt")).split("\n")
        num = tar[2]
        qq = tar[1]
        user = await return_id(qq)
        timeStamp = time.localtime(float(tar[0]))
        date = time.strftime("%Y-%m-%d",timeStamp)
        now_date = time.strftime("%Y-%m-%d",time.localtime(time.time()))
        hms = time.strftime("%H:%M:%S",timeStamp)
        if date == now_date:
            msg = f"机厅{num}人 ——{user}\n最后更新时间：{hms}"
        else:
            msg = f"今天还没有人报告机厅人数，我猜有{str(rand.randint(1,15))}"
    except Exception:
        msg = f"今天还没有人报告机厅人数，我猜有{str(rand.randint(1,15))}"
    await tj.send(msg)
