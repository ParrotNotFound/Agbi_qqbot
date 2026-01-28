from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
from nonebot import require
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="agbi_collections",
    description="银币抽奖",
    usage="/pick",
    config=Config,
)
require("plugins.file_edit")
from plugins.file_edit import read_file,append_csv_rows, read_csv_file,read_large_file, write_file, delete_file
require("plugins.agbi")
from plugins.agbi import c_coin, return_id
require("plugins.maimaidx_music")
from plugins.maimaidx_music import total_list
require("plugins.image")
from plugins.image import text_to_image2,image_to_base64
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
import aiohttp,csv

def g_collections():
    rd = rand.random()
    
    if rd <0.002:
        f = read_file(f'prize/legend.txt')
        prz = f.split('\n')
        ra = rand.randint(0,len(prz)-1)
        return ['LEGEND','传奇收藏品',prz[ra].strip('\n')]
    elif rd <0.02:
        rdsss = rand.random()
        if rdsss < 0.2:
            f = read_file(f'prize/sss.txt')
            prz = f.split('\n')
            ra = rand.randint(0,len(prz)-1)
            return ['SSS','称号',prz[ra].strip('\n')]
        else:
            dt = total_list.filter(ds=(14.7,14.9),diff=[3])
            prz = []
            for i in dt:
                prz.append(i['title'])
            ra = rand.randint(0,len(prz)-1)
            return ['SSS','歌曲',prz[ra]]
    elif rd <0.07:
        rdsss = rand.random()
        if rdsss < 0.1:
            f = read_file(f'prize/ss.txt')
            prz = f.split('\n')
            ra = rand.randint(0,len(prz)-1)
            return ['SS','称号',prz[ra].strip('\n')]
        else:
            dt = total_list.filter(ds=(14.2,14.6),diff=[3])
            prz = []
            for i in dt:
                prz.append(i['title'])
            ra = rand.randint(0,len(prz)-1)
            return ['SS','歌曲',prz[ra]]
    elif rd <0.17:
        rdsss = rand.random()
        if rdsss < 0.1:
            f = read_file(f'prize/ss.txt')
            prz = f.split('\n')
            ra = rand.randint(0,len(prz)-1)
        else:
            dt = total_list.filter(ds=(13.7,14.1),diff=[3])
            prz = []
            for i in dt:
                prz.append(i['title'])
            ra = rand.randint(0,len(prz)-1)
            return ['S','歌曲',prz[ra].strip('\n')]
    elif rd <0.4:
        rdsss = rand.random()
        if rdsss < 0.1:
            f = read_file(f'prize/a.txt')
            prz = f.split('\n')
            ra = rand.randint(0,len(prz)-1)
            return ['A','称号',prz[ra].strip('\n')]
        else:
            dt = total_list.filter(ds=(13.0,13.6),diff=[3])
            prz = []
            for i in dt:
                prz.append(i['title'])
            ra = rand.randint(0,len(prz)-1)
            return ['A','歌曲',prz[ra]]
    else:
        rdsss = rand.random()
        if rdsss < 0.5:
            p = read_file('agno3.txt').split('◈')
            prz = []
            for i in p:
                prz.append(i.replace('|','，').replace(',','，'))
            ra = rand.randint(0,len(prz)-1)
            return ['B','银币名言',prz[ra]]
        else:
            dt = total_list.filter(ds=(1,12.9),diff=[3])
            prz = []
            for i in dt:
                prz.append(i['title'])
            ra = rand.randint(0,len(prz)-1)
            return ['B','歌曲',prz[ra]]

backpack = on_command('pack',aliases = {'收集品背包'})
@backpack.handle()
async def _(event: Event, message: Message = CommandArg()):
    user_id = event.get_user_id()
    user = await return_id(str(user_id))
    msg = f'{user}的背包：'
    try:
        #with open(f'src/users/coin/{str(event.get_user_id())}.txt','r') as f:
        c = read_file(f'coin/{str(event.get_user_id())}.txt')
            #print(c)
        coin = int(c)
    except FileNotFoundError:
        coin = 0
        write_file(f'coin/{str(event.get_user_id())}.txt',str(coin))
        #await pick_card.send('银币不足！')
    msg+=f'\n银币数：{coin}'
    try:
        col_type = {'LEGEND':0,'SSS':0,'SS':0,'S':0,'A':0,'B':0}
        h_data = read_csv_file(f'collections/{str(event.get_user_id())}.csv')
        for i in range(1,len(h_data)):
            col_type[h_data[i][0]]+=1
        tot = 0
        for c in col_type:
            tot += col_type[c]
        msg += f'\n总收集品数：{tot}'
        for c in col_type:
            msg += f'\n- {c}：{col_type[c]}'
    except FileNotFoundError:
        msg += f'\n暂无收集品'
    await backpack.send(msg)


pick_card = on_command('pick')
@pick_card.handle()
async def _(event: Event, message: Message = CommandArg()):
    user_id = event.get_user_id()
    user = await return_id(str(user_id))
    u = str(message).strip(' ')
    try:
        u = int(u)
        if u <= 0:
            raise
    except Exception:
        u = 1
        #possible bug:u = 0
    try:
        #with open(f'src/users/coin/{str(event.get_user_id())}.txt','r') as f:
        c = read_file(f'coin/{str(event.get_user_id())}.txt')
            #print(c)
        coin = int(c)
            #print(coin)
            #print(u)
        if coin >= u:
            coin -= u
            msg=f'{user}获得的收集品：'
            adc = []
            for i in range(u):
                tgt = g_collections()
                adc.append(tgt)
                tmp = f'[{tgt[0]}] '
                if tgt[1] == '歌曲':
                    tmp += '「'
                    tmp+=str(tgt[2])
                    tmp += '」'
                elif tgt[1] == '银币名言':
                    tmp += '"'
                    tmp+=str(tgt[2])
                    tmp += '"'
                else:
                    tmp+=str(tgt[2])
                msg += f'\n{tmp}'
            if len(adc) <= 1:
                try:
                    await pick_card.send(msg)
                except Exception as e:
                    print(msg)
                    await pick_card.send("消息被风控，抽奖无效。")
                    return
            else:
                #print(str(image_to_base64(text_to_image2(msg)), encoding='utf-8'))
                try:
                    this_image = MessageSegment.image(file=f"base64://{str(image_to_base64(text_to_image2(msg)), encoding='utf-8')}")
                    await pick_card.send(this_image)
                except Exception as e:
                    print(e)
                    await pick_card.send("出现了错误，无法发送图片，尝试以文字方式发送消息……")
                    
                    if len(adc)<=10:
                        try:
                            await pick_card.send(msg)
                        except Exception:
                            await pick_card.send("消息被风控，抽奖无效。可能是因为信息过长")
                            return
                    else:
                        await pick_card.send("为防止刷屏及长消息被拦截，本次抽奖无效")
                        return
                    
                #await pick_card.send('[CQ:image,file=4c7895f89bb9b6a499560e058508c1c8.image,subType=0,url=https://gchat.qpic.cn/gchatpic_new/3187662862/715405137-2448148670-4C7895F89BB9B6A499560E058508C1C8/0?term=2&amp;is_origin=0]')
            append_csv_rows(f'collections/{str(event.get_user_id())}.csv',['level','category','name'],adc)
            
            '''try:
                with open(f'src/users/collections/{str(event.get_user_id())}.csv','r',encoding='utf-8') as f:
                    reader = csv.reader(f)
                with open(f'src/users/collections/{str(event.get_user_id())}.csv','a',newline='',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    for c in adc:
                        writer.writerow(c)
            except FileNotFoundError:
                #print(e)
                with open(f'src/users/collections/{str(event.get_user_id())}.csv','a',newline='',encoding='utf-8') as f:
                    writer = csv.writer(f)
                    writer.writerow(['level','category','name'])
                    for c in adc:
                        writer.writerow(c)'''

                    
            write_file(f'coin/{str(event.get_user_id())}.txt',str(coin))
        else:
            await pick_card.send('银币不足！问银币bot问题可以获取银币')
    except FileNotFoundError:
        coin = 0
        write_file(f'coin/{str(event.get_user_id())}.txt',str(coin))
        await pick_card.send('银币不足！问银币bot问题可以获取银币')
    #except Exception as e:
        #print(e)
