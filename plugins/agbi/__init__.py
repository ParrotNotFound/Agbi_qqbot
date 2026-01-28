from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import require
from .config import Config

require("plugins.file_edit")
from plugins.file_edit import read_file, read_large_file, write_file, delete_file

__plugin_meta__ = PluginMetadata(
    name="agbi",
    description="银币核心功能之银币怎么看",
    usage="银币怎么看",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot.rule import to_me, startswith
from nonebot.plugin import on_command,on_message
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters.qq import Message
from nonebot.adapters import Event
from nonebot.log import logger

import time
import random as rand
import aiohttp

version = on_command('about')

@version.handle()
async def handle_function(event: Event):
    msg = '''Agbi_bot ver1.5
    银币（测试版）上线官方qq平台
    目前仍在测试阶段 只有一小部分纯文本功能开放
    '''
    await version.send(msg)

agno3 = on_message(
    rule=startswith("银币怎么"),  # 或用 to_me() + startswith() 组合规则
    priority=5
)

@agno3.handle()
async def handle_function(event: Event):
    user_id = event.get_user_id()
    n = read_file("agno3.txt")
    agno3_list = n.split('◈')
    print(len(agno3_list))
    ra = rand.randint(0,len(agno3_list)-1)
    msg = agno3_list[ra].split('|')
    for i in msg:
        await agno3.send(i)
        time.sleep(0.1)
    try:
        c = read_file(f'coin/{user_id}.txt')
        #print(c)
        coin = int(c)
        coin += 1
        write_file(f'coin/{user_id}.txt',str(coin))
    except:
        coin = 1
        write_file(f'coin/{user_id}.txt',str(coin))

agno3_add = on_command('agno3_add')
@agno3_add.handle()
async def _(event: Event, message: Message = CommandArg()):
    u = str(message).strip(' ')
    n = read_file("agno3.txt")
    if rand.random()>0.1:
        write_file('agno3.txt',n+'◈'+u)
        await agno3_add.send(f'已添加新的名言"{u}"')
    else:
        await agno3_add.send('别啥都加没意思')
        write_file('agno3.txt',n+'◈'+u)

def agno3_said():
    n = read_file("agno3.txt")
    agno3_list = n.split('◈')
    ra = rand.randint(0,len(agno3_list)-1)
    return agno3_list[ra]

def c_coin(userqq,val):
    try:
        c = read_file(f'coin/{userqq}.txt')
        coin = int(c)
        coin += val
        if coin >= 0:
            write_file(f'coin/{userqq}.txt',str(coin))
        return coin
    except FileNotFoundError:
        coin = val
        if val >= 0:
            with open(f'src/users/coin/{userqq}.txt','w') as f:
                f.write(str(coin))
        return coin
    
async def return_id(qq):
    payload = {'qq': qq,'b50':  True}
    user = qq
    userid = qq
    try:
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
            if resp.status == 400:
                user = qq
            if resp.status == 403:
                user = qq
            else:
                obj = await resp.json()
                user = obj["nickname"]
    except Exception as e:
        print(e)
        user = qq
    return user