from pathlib import Path
import time
from typing import Any, Dict, List

import aiohttp
import nonebot
from nonebot import require
from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata
require("plugins.image")
from plugins.image import text_to_image, text_to_image2,text_to_image3,image_to_base64
require("plugins.maimaidx_music")
from plugins.maimaidx_music import Music,MusicList,total_list,Chart,get_cover_len5_id
require("plugins.file_edit")
from plugins.file_edit import read_file,append_csv_rows, read_csv_file,read_large_file, write_file, delete_file

require("plugins.agbi")
from plugins.agbi import c_coin
from .config import Config

__plugin_meta__ = PluginMetadata(
    name="maimaidx_agbi",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
from nonebot.rule import to_me, startswith
from nonebot.plugin import on_command,on_message,on_regex
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters.qq import Message, MessageSegment
#from nonebot.adapters.console import Message, MessageEvent
from nonebot.adapters import Event
from nonebot.log import logger
import math,re
import random as rand

sub_plugins = nonebot.load_plugins(
    str(Path(__file__).parent.joinpath("plugins").resolve())
)
from plugins.maimaidx_agbi.plugins.maimai_best_50 import generate50
from plugins.maimaidx_agbi.plugins.maimai_best_50_new import generate50new,get_cover_len5_id

cfq = on_command('查分器网站')


@cfq.handle()
async def _(event: Event, message: Message = CommandArg()):
    await cfq.send("https://www.diving-fish.com/maimaidx/prober/")


def computeRa(ds: float, achievement: float) -> int:
    baseRa = 22.4 
    if achievement < 50:
        baseRa = 7.0
    elif achievement < 60:
        baseRa = 8.0 
    elif achievement < 70:
        baseRa = 9.6 
    elif achievement < 75:
        baseRa = 11.2 
    elif achievement < 80:
        baseRa = 12.0 
    elif achievement < 90:
        baseRa = 13.6 
    elif achievement < 94:
        baseRa = 15.2 
    elif achievement < 97:
        baseRa = 16.8 
    elif achievement < 98:
        baseRa = 20.0 
    elif achievement < 99:
        baseRa = 20.3
    elif achievement < 99.5:
        baseRa = 20.8 
    elif achievement < 100:
        baseRa = 21.1 
    elif achievement < 100.5:
        baseRa = 21.6 

    return math.floor(ds * (min(100.5, achievement) / 100) * baseRa)

calc_score = on_command('calc', aliases={'mai calc'})


@calc_score.handle()
async def _(event: Event, message: Message = CommandArg()):
    argv = str(message).strip().split(" ")
    if len(argv) != 2:
        await calc_score.finish("命令格式为\n!calc <定数> <分数>")
        return
    try:
        ds = float(argv[0])
        score = float(argv[1])
        if ds < 1 or ds > 15.0:
            await calc_score.send("定数超出范围！")
            return
        if score < 0 or score > 101:
            await calc_score.send("分数超出范围！请输入在0~101之间的分数")
            return
        ra = computeRa(ds,score)
        totra = ra * 50
        if(totra>16200):
            totra = "16200+"
        await calc_score.send(f"{ds}达成{score}时的分数为：{ra}\n相当于{totra}的总Rating")
    except Exception as e:
        await calc_score.send(f"计算时发生错误：{str(e)}")

def lowerRank(achievement: float) -> float:
    baseRa = 100.5
    if achievement < 50:
        baseRa = 0
    elif achievement < 60:
        baseRa = 50 
    elif achievement < 70:
        baseRa = 60 
    elif achievement < 75:
        baseRa = 70 
    elif achievement < 80:
        baseRa = 75 
    elif achievement < 90:
        baseRa = 80 
    elif achievement < 94:
        baseRa = 90 
    elif achievement < 97:
        baseRa = 94 
    elif achievement < 98:
        baseRa = 97 
    elif achievement < 99:
        baseRa = 98
    elif achievement < 99.5:
        baseRa = 99 
    elif achievement < 100:
        baseRa = 99.5 
    elif achievement < 100.5:
        baseRa = 100 
    return baseRa

def upperRank(achievement: float) -> float:
    baseRa = 101
    if achievement < 50:
        baseRa = 50
    elif achievement < 60:
        baseRa = 60 
    elif achievement < 70:
        baseRa = 70 
    elif achievement < 75:
        baseRa = 75 
    elif achievement < 80:
        baseRa = 80 
    elif achievement < 90:
        baseRa = 90 
    elif achievement < 94:
        baseRa = 94 
    elif achievement < 97:
        baseRa = 97 
    elif achievement < 98:
        baseRa = 98 
    elif achievement < 99:
        baseRa = 99
    elif achievement < 99.5:
        baseRa = 99.5 
    elif achievement < 100:
        baseRa = 100 
    elif achievement < 100.5:
        baseRa = 100.5
    return baseRa

def computeRaPlus(ds: float, achievement: float) -> int:
    baseRa = 22.4
    upperRa = 23.5
    if achievement < 50:
        baseRa = 7.0
        upperRa = 8.0
    elif achievement < 60:
        baseRa = 8.0
        upperRa = 9.6
    elif achievement < 70:
        baseRa = 9.6
        upperRa = 11.2
    elif achievement < 75:
        baseRa = 11.2
        upperRa = 12.0
    elif achievement < 80:
        baseRa = 12.0
        upperRa = 13.6
    elif achievement < 90:
        baseRa = 13.6
        upperRa = 15.2
    elif achievement < 94:
        baseRa = 15.2
        upperRa = 16.8
    elif achievement < 97:
        baseRa = 16.8
        upperRa = 20.0
    elif achievement < 98:
        baseRa = 20.0
        upperRa = 20.3
    elif achievement < 99:
        baseRa = 20.3
        upperRa = 20.8
    elif achievement < 99.5:
        baseRa = 20.8
        upperRa = 21.1
    elif achievement < 100:
        baseRa = 21.1
        upperRa = 21.6
    elif achievement < 100.5:
        baseRa = 21.6
        upperRa = 22.4

    rank = lowerRank(achievement)
    upRank = upperRank(achievement)
    nowRankRa = math.floor(ds * (rank / 100.0) * baseRa)
    nextRankRa = math.floor(ds * (upRank / 100.0) * upperRa)
    return math.floor(nowRankRa + (achievement-rank) / (upRank-rank) * (nextRankRa-nowRankRa))

def computeRank(achievement: float) -> str:
    baseRa = 'sssp'
    if achievement < 50:
        baseRa = 'd'
    elif achievement < 60:
        baseRa = 'c'
    elif achievement < 70:
        baseRa = 'b'
    elif achievement < 75:
        baseRa = 'bb' 
    elif achievement < 80:
        baseRa = 'bbb' 
    elif achievement < 90:
        baseRa = 'a' 
    elif achievement < 94:
        baseRa = 'aa' 
    elif achievement < 97:
        baseRa = 'aaa' 
    elif achievement < 98:
        baseRa = 's' 
    elif achievement < 99:
        baseRa = 'sp'
    elif achievement < 99.5:
        baseRa = 'ss'
    elif achievement < 100:
        baseRa = 'ssp' 
    elif achievement < 100.5:
        baseRa = 'sss'

    return baseRa


def song_txt(music: Music):
    ds = []
    for i in music.ds:
        ds.append(str(i))
    try:
        import urllib.request
        cover_url = f"https://www.diving-fish.com/covers/{get_cover_len5_id(music.id)}.png"
        urllib.request.urlopen(cover_url)
        return Message([
            MessageSegment("text", {
                "text": f"{music.id}. {music.title}\n"
            }),
            MessageSegment("image", {
                "file": f"https://www.diving-fish.com/covers/{get_cover_len5_id(music.id)}.png"
            }),
            MessageSegment("text", {
                "text": f"\n{'/'.join(ds)}"
            })
        ])
    except:
        return Message([
            MessageSegment("text", {
                "text": f"{music.id}. {music.title}\n"
            }),
            MessageSegment("text", {
                "text": f"\n{'/'.join(ds)}"
            })
        ])


def inner_level_q(ds1, ds2=None):
    result_set = []
    diff_label = ['Bas', 'Adv', 'Exp', 'Mst', 'ReM']
    if ds2 is not None:
        music_data = total_list.filter(ds=(ds1, ds2))
    else:
        music_data = total_list.filter(ds=ds1)
    for music in sorted(music_data, key = lambda i: int(i['id'])):
        for i in music.diff:
            result_set.append((music['id'], music['title'], music['ds'][i], diff_label[i], music['level'][i]))
    return result_set

#ver1.0.1
async def local_update_score(payload: Dict):
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            return 400
        if resp.status == 403:
            return 403
        
        obj = await resp.json()
        #print(obj)
        dx: List[Dict] = obj["charts"]["dx"]
        sd: List[Dict] = obj["charts"]["sd"]
        msg = ''
        tar = ['nan',0,0,0,0,'nan']
        try:
            h_data = read_csv_file(f'{obj["username"]}.csv')
            tar = ['nan',0,0,0,0,'nan']
            c_time = time.time()-604800
            for i in range(1,len(h_data)):
               if abs(float(h_data[i][4])-c_time) < abs(float(tar[4])-c_time):
                    tar = h_data[i]
                    #print(tar)
            tar[1] = int(tar[1])
            for i in range(2,5):
                tar[i] = float(tar[i])
        except FileNotFoundError as e:
            print(e)   
        plt = ''
        if obj["plate"] != '':
            plt = '['+ obj["plate"] +']'
        msg += f'{obj["nickname"]} {plt}\nDX Rating：{obj["rating"]} (+{obj["rating"]-tar[1]})\n'
        cnt = 0
        tot_acc=0
        tot_dxscore=0
        max_dxscore=0
        avg_acc = '0.0000'
        avg_dxscore = '0.0000'
        stars = ''
        if True:
            for c in sd:
                cnt+=1
                
                tot_acc += c['achievements']
                tot_dxscore += c['dxScore']
                #print(c['song_id'])
                music = total_list.by_id(str(c['song_id']))
                #print(c['level_index'])
                #print(music)
                chart: Dict[Any] = music['charts'][c['level_index']]
                tap = int(chart['notes'][0])
                slide = int(chart['notes'][2])
                hold = int(chart['notes'][1])
                touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
                brk = int(chart['notes'][-1])
                
                max_dxscore += 3*(tap+slide+hold+touch+brk)

                
            for c in dx:
                cnt+=1
                
                tot_acc += c['achievements']
                tot_dxscore += c['dxScore']
                #print(c['song_id'])
                music = total_list.by_id(str(c['song_id']))
                #print(c['level_index'])
                #print(music)
                chart: Dict[Any] = music['charts'][c['level_index']]
                tap = int(chart['notes'][0])
                slide = int(chart['notes'][2])
                hold = int(chart['notes'][1])
                touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
                brk = int(chart['notes'][-1])
                
                max_dxscore += 3*(tap+slide+hold+touch+brk)
            if cnt > 0:
                avg_acc = format((tot_acc/cnt),'.4f')
                avg_dxscore = format((tot_dxscore / max_dxscore*100.0),'.4f')
                
                fld = float(avg_dxscore)
                if fld > 85:
                    stars += '✦'
                if fld > 90:
                    stars += '✦'
                if fld > 93:
                    stars += '✦'
                if fld > 95:
                    stars += '✦'
                if fld > 97:
                    stars += '✦'
                if fld > 99:
                    stars += '✦'
            v_acc = float(format((tot_acc/cnt)-tar[2],".4f"))
            if v_acc >= 0:
                v_acc = '+'+str(v_acc)
            else:
                v_acc = str(v_acc)
                
            v_dxacc = float(format((tot_dxscore / max_dxscore*100.0)-tar[3],".4f"))
            if v_dxacc >= 0:
                v_dxacc = '+'+str(v_dxacc)
            else:
                v_dxacc = str(v_dxacc)
                
            msg+=f'准确度：{avg_acc}% ({v_acc}%)\nDX分数准度：{avg_dxscore}% {stars} ({v_dxacc}%)'
            
            if len(dx)>=1 and len(sd)>=1:
                if dx[0]['ra']<=sd[0]['ra']:
                    bpl = sd[0]
                else:
                    bpl = dx[0]
            elif len(sd)>=1:
                bpl = sd[0]
            elif len(dx)>=1:
                bpl = dx[0]
            #print(bpl)
            ra = 0
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            try:
                set_best = read_file(f'best_score/{obj["nickname"]}.txt').split('\n')
                level_index = int(set_best[1])
                name = set_best[0]
                title = set_best[2]
                music = total_list.by_id(str(name))
                chart = music['charts'][level_index]
                ds = music['ds'][level_index]
                score = set_best[3]
                ra = computeRa(float(ds),float(score))
                msg+=f'\n置顶成绩：\n{title} | {level_name[level_index]} {ds}\n{format(float(score),".4f")}% Rating:{ra}'
            except Exception as err:
                print(err)
                try:
                    level_index = bpl['level_index']
                    name = bpl['song_id']
                    music = total_list.by_id(str(name))
                    print(music)
                    chart = music['charts'][level_index]
                    ds = music['ds'][level_index]
                    level = music['level'][level_index]
                            #file = f"https://www.diving-fish.com/covers/{get_cover_len4_id(music['id'])}.png"
                    ra = bpl['ra']
                    msg+=f'\n最佳成绩：\n{bpl["title"]} | {level_name[level_index]} {ds}\n{format(bpl["achievements"],".4f")}% Rating:{ra}'
                except Exception as e:
                    print(e)
                
            obj_data = {'nickname':[obj["nickname"]],'rating':[obj["rating"]],'acc':[float(avg_acc)],'DX Score acc':[float(avg_dxscore)],'timestamp':[time.time()],'date':[time.asctime()]}
            #'nickname','rating','acc','DX Score acc','timestamp','date'
            ret = append_csv_rows(f'{obj["username"]}.csv',['nickname','rating','acc','DX Score acc','timestamp','date'],[[obj["nickname"],obj["rating"],float(avg_acc),float(avg_dxscore),time.time(),time.asctime()]])
            print(ret)
        #pic = DrawBest(sd_best, dx_best, obj["nickname"]).getDir()
        return msg

set_topscore = on_command('top',aliases={'置顶','设置置顶'})
@set_topscore.handle()
async def _(event: Event, message: Message = CommandArg()):
    argv = str(message).strip().split(" ")
    #print(argv)
    if len(argv) == 0 or len(argv) > 2 or (len(argv) == 1 and argv[0] == ''):
        await inner_level.finish("命令格式为\n/top [难度]id[id] (分数)\n如：/top 白id825 或 /top 白id825 100.2099")
        return
    
    try:
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
            if resp.status == 400:
                await player_raPlus.finish("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
            elif resp.status == 403:
                await player_raPlus.finish("该用户禁止了其他人获取数据。")
            obj = await resp.json()
            if len(argv) == 1 and argv[0] == 'reset':
                data = f''
                write_file(f'best_score/{obj["nickname"]}.txt',data)
                await inner_level.send("已重置置顶分数")
                return
            regex = "([绿黄红紫白]?)id([0-9]+)"
            groups = re.match(regex, str(argv[0])).groups()
            name = groups[1]
            level_labels = ['绿', '黄', '红', '紫', '白']
            level_index = level_labels.index(groups[0])
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            
            if len(argv) == 1:
                dx: List[Dict] = obj["charts"]["dx"]
                sd: List[Dict] = obj["charts"]["sd"]
                for c in dx:
                    if str(c['song_id']) == name and str(level_index) == str(c['level_index']):
                        data = f'{name}\n{level_index}\n{c["title"]}\n{format(c["achievements"],".4f")}'
                        write_file(f'best_score/{obj["nickname"]}.txt',data)
                        await set_topscore.send(f"更新置顶成绩成功：{c['title']}")
                        return
                for c in sd:
                    if str(c['song_id']) == name and str(level_index) == str(c['level_index']):
                        data = f'{name}\n{level_index}\n{c["title"]}\n{format(c["achievements"],".4f")}'
                        write_file(f'best_score/{obj["nickname"]}.txt',data)
                        await set_topscore.send(f"更新置顶成绩成功：{c['title']}")
                        return
                await set_topscore.send(f"你的b50里未出现该成绩，请手动输入分数")
                return
            elif len(argv) == 2:
                #name = groups[1]
                music = total_list.by_id(name)
                data = f'{name}\n{level_index}\n{music["title"]}\n{format(float(argv[1]),".4f")}'
                write_file(f'best_score/{obj["nickname"]}.txt',data)
                await set_topscore.send(f"更新置顶成绩成功：{music['title']}")
                return
    except Exception as e:
        await set_topscore.finish(f"出现错误：{str(e)}")

search_music = on_regex(r"^查歌.+")


@search_music.handle()
async def _(event: Event, message: Message = EventMessage()):
    regex = "查歌(.+)"
    name = re.match(regex, str(message)).groups()[0].strip()
    if name == "":
        return
    res = total_list.filter(title_search=name)
    if len(res) == 0:
        await search_music.send("没有找到这样的乐曲。")
    elif len(res) < 50:
        search_result = ""
        for music in sorted(res, key = lambda i: int(i['id'])):
            search_result += f"{music['id']}. {music['title']}\n"
        await search_music.finish(Message([
            MessageSegment("text", {
                "text": search_result.strip()
            })]))
    else:
        await search_music.send(f"结果过多（{len(res)} 条），请缩小查询范围。")

query_chart = on_regex(r"^([绿黄红紫白]?)id([0-9]+)")


@query_chart.handle()
async def _(event: Event, message: Message = EventMessage()):
    regex = "([绿黄红紫白]?)id([0-9]+)"
    groups = re.match(regex, str(message)).groups()
    level_labels = ['绿', '黄', '红', '紫', '白']
    if groups[0] != "":
        try:
            level_index = level_labels.index(groups[0])
            level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
            name = groups[1]
            music = total_list.by_id(name)
            chart = music['charts'][level_index]
            ds = music['ds'][level_index]
            level = music['level'][level_index]
            file = f"https://www.diving-fish.com/covers/{get_cover_len4_id(music['id'])}.png"
            if len(chart['notes']) == 4:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
BREAK: {chart['notes'][3]}
谱师: {chart['charter']}'''
            else:
                msg = f'''{level_name[level_index]} {level}({ds})
TAP: {chart['notes'][0]}
HOLD: {chart['notes'][1]}
SLIDE: {chart['notes'][2]}
TOUCH: {chart['notes'][3]}
BREAK: {chart['notes'][4]}
谱师: {chart['charter']}'''
            await query_chart.send(Message([
                MessageSegment("text", {
                    "text": f"{music['id']}. {music['title']}\n"
                }),
                MessageSegment("image", {
                    "file": f"{file}"
                }),
                MessageSegment("text", {
                    "text": msg
                })
            ]))
        except Exception:
            await query_chart.send("未找到该谱面")
    else:
        name = groups[1]
        music = total_list.by_id(name)
        try:
            file =f"https://www.diving-fish.com/covers/{get_cover_len4_id(music['id'])}.png"
            await query_chart.send(Message([
                MessageSegment("text", {
                    "text": f"{music['id']}. {music['title']}\n"
                }),
                MessageSegment("image", {
                    "file": f"{file}"
                }),
                MessageSegment("text", {
                    "text": f"艺术家: {music['basic_info']['artist']}\n分类: {music['basic_info']['genre']}\nBPM: {music['basic_info']['bpm']}\n版本: {music['basic_info']['from']}\n难度: {'/'.join(music['level'])}"
                })
            ]))
        except Exception:
            await query_chart.send("未找到该乐曲")
#ver1.0.1


inner_level = on_command('inner_level ', aliases={'定数查歌 '})

@inner_level.handle()
async def _(event: Event, message: Message = CommandArg()):
    argv = str(message).strip().split(" ")
    if len(argv) > 2 or len(argv) == 0:
        await inner_level.finish("命令格式为\n定数查歌 <定数>\n定数查歌 <定数下限> <定数上限>")
        return
    if len(argv) == 1:
        result_set = inner_level_q(float(argv[0]))
    else:
        result_set = inner_level_q(float(argv[0]), float(argv[1]))
    if len(result_set) > 50:
        await inner_level.finish(f"结果过多（{len(result_set)} 条），请缩小搜索范围。")
        return
    s = ""
    for elem in result_set:
        s += f"{elem[0]}. {elem[1]} {elem[3]} {elem[4]}({elem[2]})\n"
    await inner_level.finish(s.strip())

spec_rand = on_regex(r"^随个(?:dx|sd|标准)?[绿黄红紫白]?[0-9]+\+?")

@spec_rand.handle()
async def _(event: Event, message: Message = EventMessage()):
    level_labels = ['绿', '黄', '红', '紫', '白']
    regex = "随个((?:dx|sd|标准))?([绿黄红紫白]?)([0-9]+\+?)"
    res = re.match(regex, str(message).lower())
    try:
        if res.groups()[0] == "dx":
            tp = ["DX"]
        elif res.groups()[0] == "sd" or res.groups()[0] == "标准":
            tp = ["SD"]
        else:
            tp = ["SD", "DX"]
        level = res.groups()[2]
        if res.groups()[1] == "":
            music_data = total_list.filter(level=level, type=tp)
        else:
            music_data = total_list.filter(level=level, diff=['绿黄红紫白'.index(res.groups()[1])], type=tp)
        if len(music_data) == 0:
            rand_result = "没有这样的乐曲哦。"
        else:
            rand_result = song_txt(music_data.random())
        await spec_rand.send(rand_result)
    except Exception as e:
        print(e)
        await spec_rand.finish("随机命令错误，请检查语法")




ping = on_command('ping')
@ping.handle()
async def _(event: Event, message: Message = CommandArg()):
    username = str(message).strip()
    
    payload = {'qq': str(event.get_user_id())}
    try:
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
            if resp.status == 400:
                await ping.send("正常访问，返回400")
            if resp.status == 403:
                await ping.send("正常访问，返回403")
            else:
                await ping.send("正常访问")
                obj = await resp.json()
                print(str(obj))
    except Exception as e:
        await ping.send(str(e))

wm_list = ['拼机', '推分', '越级', '下埋', '早勤','夜勤', '练底力', '练手法', '打儿歌', '摆烂','干饭', '抓绝赞', '收歌','睡觉','早起','录手元','查分','看谱面确认']


jrwm = on_command('今日舞萌', aliases={'今日mai'})


@jrwm.handle()
async def _(event: Event, message: Message = CommandArg()):
    #c_coin(str(event.get_user_id()),rand.randint(1,4))
    qq = int(event.get_user_id())
    h = hash(qq)
    rp = h % 100
    c = h
    wm_value = []
    for i in range(18):
        wm_value.append(c & 7)
        c >>= 2
    s = f"今日人品值：{rp}\n"
    for i in range(18):
        if wm_value[i] == 3:
            s += f'宜 {wm_list[i]}\n'
        elif wm_value[i] == 0:
            s += f'忌 {wm_list[i]}\n'
    s += "银币提醒您：打机时不要大力拍打或滑动哦\n今日推荐歌曲："
    music = total_list[h % len(total_list)]
    await jrwm.finish(Message([MessageSegment("text", {"text": s})] + song_txt(music)))

query_score = on_command('分数线')


@query_score.handle()
async def _(event: Event, message: Message = CommandArg()):
    r = "([绿黄红紫白])(id)?([0-9]+)"
    argv = str(message).strip().split(" ")
    if len(argv) == 1 and argv[0] == '帮助':
        s = '''此功能为查找某首歌分数线设计。
命令格式：分数线 <难度+歌曲id> <分数线>
例如：分数线 紫799 100
命令将返回分数线允许的 TAP GREAT 容错以及 BREAK 50落等价的 TAP GREAT 数。
以下为 TAP GREAT 的对应表：
GREAT/GOOD/MISS
TAP\t1/2.5/5
HOLD\t2/5/10
SLIDE\t3/7.5/15
TOUCH\t1/2.5/5
BREAK\t5/12.5/25(外加200落)'''
        await query_score.send(Message([
            MessageSegment("image", {
                "file": f"base64://{str(image_to_base64(text_to_image(s)), encoding='utf-8')}"
            })
        ]))
    elif len(argv) == 2:
        try:
            grp = re.match(r, argv[0]).groups()
            level_labels = ['绿', '黄', '红', '紫', '白']
            level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
            level_index = level_labels.index(grp[0])
            chart_id = grp[2]
            line = float(argv[1])
            music = total_list.by_id(chart_id)
            chart: Dict[Any] = music['charts'][level_index]
            tap = int(chart['notes'][0])
            slide = int(chart['notes'][2])
            hold = int(chart['notes'][1])
            touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
            brk = int(chart['notes'][-1])
            total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
            break_bonus = 0.01 / brk
            break_50_reduce = total_score * break_bonus / 4
            reduce = 101 - line
            if reduce <= 0 or reduce >= 101:
                raise ValueError
            await query_score.send(f'''{music['title']} {level_labels2[level_index]}
分数线 {line}% 允许的最多 TAP GREAT 数量为 {(total_score * reduce / 10000):.2f}(每个-{10000 / total_score:.4f}%),
BREAK 50落(一共{brk}个)等价于 {(break_50_reduce / 100):.3f} 个 TAP GREAT(-{break_50_reduce / total_score * 100:.4f}%)''')
        except Exception:
            await query_score.send("格式错误，输入“分数线 帮助”以查看帮助信息")


player_info = on_message(
    rule=startswith(('～','~'), ignorecase=False),  # 或用 to_me() + startswith() 组合规则
    priority=5
)
@player_info.handle()
async def _(event: Event):
    msg = ""
    print(str(event.get_user_id()))
    payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    resp = await local_update_score(payload)
    #async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
    if resp == 400:
        await player_info.finish("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
    elif resp == 403:
        await player_info.finish("该用户禁止了其他人获取数据。")
    else:
        await player_info.finish(resp)




player_raPlus = on_command('raplus',aliases = {'raplus','raplus'})
@player_raPlus.handle()
async def _(event: Event, message: Message = CommandArg()):
    msg = ""
    
    username = str(message).strip()
    if username == "":
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    else:
        payload = {'username': username,'b50':  True}
    
    
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            await player_raPlus.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
        if resp.status == 403:
            await player_raPlus.send("该用户禁止了其他人获取数据。")
        else:
            obj = await resp.json()
            msg = ''
            async with aiohttp.request("GET", "https://www.diving-fish.com/api/maimaidxprober/chart_stats") as resp2:
                stats = await resp2.json()
                dx: List[Dict] = obj["charts"]["dx"]
                sd: List[Dict] = obj["charts"]["sd"]
                raPlus = 0
                maxRa = 0
                maxdiff = 0
                for c in sd:
                    try:
                        diff = stats['charts'][str(c['song_id'])][c['level_index']]["fit_diff"]
                    except Exception:
                        diff = c['ds']
                    single = computeRaPlus(diff,c['achievements'])
                    if single > maxRa:
                        maxRa = single
                        maxdiff = diff
                        bpl = c
                    raPlus += computeRaPlus(diff,c['achievements'])
                for c in dx:
                    try:
                        diff = stats['charts'][str(c['song_id'])][c['level_index']]["fit_diff"]
                    except Exception:
                        diff = c['ds']
                    single = computeRaPlus(diff,c['achievements'])
                    if single > maxRa:
                        maxRa = single
                        maxdiff = diff
                        bpl = c
                    raPlus += computeRaPlus(diff,c['achievements']) 
            try:
                level_index = bpl['level_index']
                level_name = ['Basic', 'Advanced', 'Expert', 'Master', 'Re: MASTER']
                name = bpl['song_id']
                music = total_list.by_id(str(name))
                print(music)
                chart = music['charts'][level_index]
                ds = music['ds'][level_index]
                level = music['level'][level_index]
                        #file = f"https://www.diving-fish.com/covers/{get_cover_len4_id(music['id'])}.png"
                ra = bpl['ra']
                msg+=f'\n最佳成绩：\n{bpl["title"]} | {level_name[level_index]} {level} ({format(maxdiff,".2f")}) \n{format(bpl["achievements"],".4f")}% RatingPlus:{maxRa}'
            except Exception as e:
                print(e)
            #raPlus = await player_raPlus(obj)
            await player_raPlus.send(f"{obj['nickname']}\nDX Rating：{obj['rating']}\nRatingPlus：{raPlus}{msg}")

best_50_pic = on_command('b50')


@best_50_pic.handle()
async def _(event: Event, message: Message = CommandArg()):
    username = str(message).strip()
    if username == "":
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    else:
        payload = {'username': username,'b50':  True}
    img, success = await generate50(payload)
    if success == 400:
        await best_50_pic.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
    elif success == 403:
        await best_50_pic.send("该用户禁止了其他人获取数据。")
    else:
        await local_update_score(payload)
        await best_50_pic.send(Message([
            MessageSegment("image", {
                "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            })
        ]))
    
    c_coin(str(event.get_user_id()),rand.randint(0,4))

b50_raPlus = on_command('rp50')
@b50_raPlus.handle()
async def _(event: Event, message: Message = CommandArg()):
    msg = ""
    
    username = str(message).strip()
    if username == "":
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    else:
        payload = {'username': username,'b50':  True}
    img, success = await generate50new(payload)
    if success == 400:
        await b50_raPlus.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
    elif success == 403:
        await b50_raPlus.send("该用户禁止了其他人获取数据。")
    else:
        await local_update_score(payload)
        await b50_raPlus.send(Message([
            MessageSegment("image", {
                "file": f"base64://{str(image_to_base64(img), encoding='utf-8')}"
            })
        ]))
    c_coin(str(event.get_user_id()),rand.randint(0,3))

from io import BytesIO
from datetime import datetime
import matplotlib.dates as mdate
import matplotlib.pyplot as plt
#v1.0.2

async def song_fit_diff(song_id):
    async with aiohttp.request("GET", "https://www.diving-fish.com/api/maimaidxprober/chart_stats") as resp:
        stats = await resp.json()
        #diff = stats['charts'][str(c['song_id'])][c['level_index']]["fit_diff"]
        diff = []
        #print(stats['charts'][str(song_id)])
        for c in stats['charts'][str(song_id)]:
            #print(c)
            try:
                diff.append("{:.2f}".format(c["fit_diff"]))
            except:
                continue
        return diff

def ra_get_diff(ds,fit_ds):
    rd = fit_ds - ds
    if rd < -0.5:
        return 0
    elif rd < -0.2:
        return 1
    elif rd < 0.1:
        return 2
    elif rd < 0.4:
        return 3
    else:
        return 4


        

def antiComputeRa(ra:float) -> float:
    baseRa = 22.4 
    return ra / (100.5 / 100) / baseRa

def avail(chart_id,level_index):
    music = total_list.by_id(chart_id)
    chart: Dict[Any] = music['charts'][level_index]
    tap = int(chart['notes'][0])
    slide = int(chart['notes'][2])
    hold = int(chart['notes'][1])
    touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
    brk = int(chart['notes'][-1])
    total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
    break_bonus = 0.01 / brk
    break_50_reduce = total_score * break_bonus / 4
    reduce = 0.5
    wrongs = (total_score * reduce / 10000)
    return wrongs

def break_count(chart_id,level_index):
    music = total_list.by_id(chart_id)
    chart: Dict[Any] = music['charts'][level_index]
    tap = int(chart['notes'][0])
    slide = int(chart['notes'][2])
    hold = int(chart['notes'][1])
    touch = int(chart['notes'][3]) if len(chart['notes']) == 5 else 0
    brk = int(chart['notes'][-1])
    total_score = 500 * tap + slide * 1500 + hold * 1000 + touch * 500 + brk * 2500
    break_bonus = 0.01 / brk
    break_50_reduce = total_score * break_bonus / 4
    ret = f'{break_50_reduce / total_score * 100:.4f}'
    return [brk,ret]

def Rong_Cuo(chart_id,level_index):
    w = avail(chart_id,level_index)
    if w < 20:
        return 0
    elif w < 30:
        return 1
    elif w < 40:
        return 2
    elif w < 50:
        return 3
    else:
        return 4

async def song_txt_ra(music: Music,diff):
    ds = []
    fit_diff = await song_fit_diff(music.id)
    level_labels2 = ['Basic', 'Advanced', 'Expert', 'Master', 'Re:MASTER']
    ra_diff = ['很低','较低','中等','较高','很高']
    for i in music.ds:
        ds.append(str(i))
    try:
        import urllib.request
        cover_url = f"https://www.diving-fish.com/covers/{get_cover_len5_id(music.id)}.png"
        urllib.request.urlopen(cover_url)
        return Message([
            MessageSegment("text", {
                "text": f"{music.id}. {music.title}\n"
            }),
            MessageSegment("image", {
                "file": f"https://www.diving-fish.com/covers/{get_cover_len5_id(music.id)}.png"
            }),
            MessageSegment("text", {
                "text": f"\n{level_labels2[diff]} {ds[diff]} ({fit_diff[diff]})\nSSS：{computeRa(float(ds[diff]),100.0)}\nSSS+：{computeRa(float(ds[diff]),100.5)}\n吃分难度：{ra_diff[ra_get_diff(float(ds[diff]),float(fit_diff[diff]))]}\n容错：{ra_diff[Rong_Cuo(music.id,diff)]}({int(avail(music.id,diff))})\n绝赞个数：{break_count(music.id,diff)[0]} (50落-{break_count(music.id,diff)[1]}%)"
            })
        ])
    except:
        return Message([
            MessageSegment("text", {
                "text": f"{music.id}. {music.title}\n"
            }),
            MessageSegment("text", {
                "text": f"\n{level_labels2[diff]} {ds[diff]} ({fit_diff[diff]})\nSSS：{computeRa(float(ds[diff]),100.0)}\nSSS+：{computeRa(float(ds[diff]),100.5)}\n吃分难度：{ra_diff[ra_get_diff(float(ds[diff]),float(fit_diff[diff]))]}\n容错：{ra_diff[Rong_Cuo(music.id,diff)]}({int(avail(music.id,diff))})\n绝赞个数：{break_count(music.id,diff)[0]} (50落-{break_count(music.id,diff)[1]})"
            })
        ])

rt_recommend = on_command("suggest",aliases={"吃分推荐"})
@rt_recommend.handle()
async def _(event: Event, message: Message = CommandArg()):
    payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            await rt_recommend.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
        elif resp.status == 403:
            await rt_recommend.send("该用户禁止了其他人获取数据。")
        else:
            obj = await resp.json()
            floor = int(obj["charts"]["sd"][-1]['ra'])
            dx: List[Dict] = obj["charts"]["dx"]
            sd: List[Dict] = obj["charts"]["sd"]
            floor_ds = antiComputeRa(floor)
            musics = total_list.filter(ds=(floor_ds,floor_ds+0.8))
            for i in range(50):
                music_data = musics.random()
                ds_diffs = music_data.ds
                ds = 0
                for d in range(len(ds_diffs)):
                    if ds_diffs[d] >= floor_ds and ds_diffs[d] <= floor_ds+0.8:
                        ds = ds_diffs[d]
                        diff = d
                        if rand.random() < 0.5:
                            break
                fd = False
                if int(music_data.id) > 100000:
                    fd = True
                for c in dx:
                    if str(c['song_id']) == str(music_data.id) and str(c['ds']) == str(ds) and float(c['achievements']) >= 100.5:
                        fd = True
                        break
                for c in sd:
                    if str(c['song_id']) == str(music_data.id) and str(c['ds']) == str(ds) and float(c['achievements']) >= 100.5:
                        fd = True
                        break
                if not fd:
                    break
            msg = await song_txt_ra(music_data,diff)
            await rt_recommend.send(msg)

spec_ds_rand = on_command("ds",aliases={"定数随机","定数随歌"})

@spec_ds_rand.handle()
async def _(event: Event, message: Message = CommandArg()):
    res = str(message).split(' ')
    try:
        if len(res) < 1 or len(res) > 2:
            raise
        if len(res) == 1:
            floor_ds = res[0]
            ceil_ds = res[0]
        if len(res) == 2:
            floor_ds = res[0]
            ceil_ds = res[1]
        music_data = total_list.filter(ds=(float(floor_ds),float(ceil_ds)))
        if len(music_data) == 0:
            rand_result = "没有这样的乐曲哦。"
        else:
            music = music_data.random()
            ds_diffs = music.ds
            ds = 0
            for d in range(len(ds_diffs)):
                if ds_diffs[d] >= float(floor_ds) and ds_diffs[d] <= float(ceil_ds):
                    ds = ds_diffs[d]
                    diff = d
                    if rand.random() < 0.5:
                        break
            rand_result = await song_txt_ra(music,diff)
        await spec_ds_rand.send(rand_result)
    except Exception as e:
        print(e)
        await spec_ds_rand.finish("随机命令错误，请检查语法")


#推荐曲目
qz_list = ['PANDORA PARADOXXX','QZKago Requiem','The EmpErroR','Garakuta Doll Play','Schwarzschild']

yrj = on_command('你能推荐一首适合我的曲子吗？',aliases={'曲目推荐','推荐歌曲','推荐曲目','今天打什么歌'})
@yrj.handle()
async def _(event: Event, message: Message = CommandArg()):
    if time.time()<168039360:
        rd = int(time.time())%5
        await yrj.send(f'当然可以!我推荐一首"{qz_list[rd]}" ，因为它是一个非常适合新手入门的曲子，曲风明快轻快，适合快节奏的游戏将它设为最初挑战。无论是节奏感还是乐器演奏，都很简单易懂，还能快速提升自己的反应力以及游戏得分。无论是舞萌DX的新玩家还是有经验的老手都会因为它的可爱和简单又离不开它的。​')
    else:
        username = str(message).strip()
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
        await local_update_score(payload)
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
            if resp.status == 400:
                await yrj.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
            elif resp.status == 403:
                await yrj.send("该用户禁止了其他人获取数据。")
            else:
                obj = await resp.json()
                ra = obj["rating"] / 70
                divr = (obj["rating"] -4500)/30000+1.2
                level = min(14.9,int(ra / divr)/10)
                if level<7:
                    await yrj.send("多练练再来求推荐吧！")
                
                else:
                    print(str(level))
                    tp = ["SD", "DX"]
                    lw = format((float(level-0.21)),'.1f')
                    ur = format((float(level+0.21)),'.1f')
                    music_data = total_list.filter(ds=(float(lw),float(ur)))
                    #print(music_data)
                    rand_result = song_txt(music_data.random())
                    await spec_rand.send(rand_result)



yrja = on_command('推荐定数',aliases = {'推荐范围','曲目推荐范围'})
@yrja.handle()
async def _(event: Event, message: Message = CommandArg()):
    if time.time()<168039360:
        await yrja.send('曲目推荐范围：你猜')
    else:
        username = str(message).strip()
        payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
        await local_update_score(payload)
        async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
            if resp.status == 400:
                await yrja.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
            elif resp.status == 403:
                await yrja.send("该用户禁止了其他人获取数据。")
            else:
                obj = await resp.json()
                ra = obj["rating"] / 70
                divr = (obj["rating"] -4500)/30000+1.2
                level = min(14.9,int(ra / divr)/10)
                lw = format((float(level-0.21)),'.1f')
                ur = format((float(level+0.21)),'.1f')
                await query_chart.send(f'{obj["username"]} \n底分：{obj["rating"]}\n曲目推荐范围：{lw}~{ur}')



#谱师查询
ctr = on_command('c50',aliases = {'best c','base c','best 谱师分析','base 谱师分析'})
@ctr.handle()
async def _(event: Event, message: Message = CommandArg()):
    username = str(message).strip()
    
    payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
    await local_update_score(payload)
    async with aiohttp.request("POST", "https://www.diving-fish.com/api/maimaidxprober/query/player", json=payload) as resp:
        if resp.status == 400:
            await ctr.send("未找到此玩家，请确保此玩家的用户名和查分器中的用户名相同。*由于qq官方bot特性，请输入/bind <用户名> 绑定自己的查分器用户")
        if resp.status == 403:
            await ctr.send("该用户禁止了其他人获取数据。")
        else:
            
            
            obj = await resp.json()
            dx: List[Dict] = obj["charts"]["dx"]
            sd: List[Dict] = obj["charts"]["sd"]
            #print(dx)
            #print(sd)
            ct_list = []
            for c in sd:
                c_ra = c['ra']
                #print(c['song_id'])
                music = total_list.by_id(str(c['song_id']))
                #print(c['level_index'])
                #print(music)
                chart: Dict[Any] = music['charts'][c['level_index']]
                t_mp = chart['charter']

                notfound = True
                for t in ct_list:
                    if t[0] == t_mp:
                        notfound = False
                        t[1]+=1
                        t[2]+=c_ra
                if notfound:
                    ct_list.append([t_mp,1,c_ra])
                

                
            for c in dx:
                c_ra = c['ra']
                #print(c['song_id'])
                music = total_list.by_id(str(c['song_id']))
                #print(c['level_index'])
                #print(music)
                chart: Dict[Any] = music['charts'][c['level_index']]
                t_mp = chart['charter']

                notfound = True
                for t in ct_list:
                    if t[0] == t_mp:
                        notfound = False
                        t[1]+=1
                        t[2]+=c_ra
                if notfound:
                    ct_list.append([t_mp,1,c_ra])
                    
        ct_list.sort(key=lambda ele: ele[2],reverse=True)
        ct_msg = f'''{obj["nickname"]} 底分：{obj["rating"]}\n在您的b50中：\n'''
        for t in ct_list:
            ct_msg += f'''{t[0]} 的谱共有 {t[1]} 张，提供 {t[2]} 底分\n'''

        #await ctr.send(ct_msg)
        await ctr.send(Message([
            MessageSegment("image", {
                "file": f"base64://{str(image_to_base64(text_to_image(ct_msg)), encoding='utf-8')}"
            })
        ]))



# 常量定义
SECONDS_PER_DAY = 86400
DEFAULT_DAYS = 28
CSV_HEADER = ["nickname", "rating", "acc", "DX Score acc", "timestamp", "date"]

ra_draw = on_command(
    '底分变化图',
    aliases={'ra变化图', 'rt变化图', 'rating~', 'rating～', 'ra~', 'ra～', 'rt~', 'rt～'},
    priority=5
)

def process_history_data(raw_data: list, time_limit: int) -> tuple:
    """处理历史数据（适配新表头）"""
    dates = []
    ratings = []
    max_rating = 0
    min_rating = 17000
    
    for row in raw_data[1:]:  # 跳过表头
        try:
            # 根据新表头结构获取数据
            # ['nickname','rating','acc','DX Score acc','timestamp','date']
            timestamp = int(float(row[4]))  # timestamp在索引4
            if time.time() - timestamp > time_limit:
                continue
            
            current_date = datetime.fromtimestamp(timestamp).date()
            current_rating = int(row[1])  # rating在索引1
        except (IndexError, ValueError) as e:
            continue
        
        # 合并同日期数据取最高分
        if dates and dates[-1] == current_date:
            ratings[-1] = max(ratings[-1], current_rating)
        else:
            dates.append(current_date)
            ratings.append(current_rating)
        
        max_rating = max(max_rating, current_rating)
        min_rating = min(min_rating, current_rating)
    
    return dates, ratings, max_rating, min_rating

def generate_rating_plot(
    dates: list, 
    ratings: list, 
    max_r: int, 
    min_r: int,
    player_name: str
) -> bytes:
    """生成评分趋势图并返回二进制数据"""
    plt.figure(figsize=(9, 5), dpi=120)
    
    # 绘制趋势线
    plt.plot(dates, ratings, marker='o', linestyle='-', color='#2196F3')
    
    # 配置图表样式
    ax = plt.gca()
    ax.set_title(f"{player_name} [Rating趋势]", fontproperties="SimHei")
    ax.xaxis.set_major_formatter(mdate.DateFormatter('%Y-%m-%d'))
    ax.xaxis.set_major_locator(mdate.DayLocator(interval=7))
    
    # 设置纵坐标范围
    plt.ylim(max(min_r - 50, 0), min(max_r + 50, 17000))
    plt.grid(True, alpha=0.3)
    
    # 保存到内存
    buf = BytesIO()
    plt.savefig(buf, format='png', bbox_inches='tight', dpi=120)
    plt.close()
    buf.seek(0)
    return buf.getvalue()

@ra_draw.handle()
async def handle_ra_draw(event: Event, message: Message = CommandArg()):
    user_id = event.get_user_id()
    try:
        # 解析时间参数
        days_input = str(message).strip()
        days_limit = int(days_input) if days_input.isdigit() else DEFAULT_DAYS
        time_limit = days_limit * SECONDS_PER_DAY
        
        # 获取玩家数据
        player_data = await fetch_player_data(user_id)
        username = player_data["username"]
        
        # 读取历史数据
        csv_data = await read_csv_file(f"{username}.csv")
        if isinstance(csv_data, str):
            raise FileNotFoundError(csv_data)
        
        # 处理数据
        dates, ratings, max_r, min_r = process_history_data(csv_data, time_limit)
        if len(ratings) < 2:
            raise ValueError("数据不足，至少需要2个有效数据点")
        
        # 生成并发送图表
        image_bytes = generate_rating_plot(dates, ratings, max_r, min_r, player_data["nickname"])
        await ra_draw.send(MessageSegment.image(image_bytes))
        
    except FileNotFoundError:
        await ra_draw.finish("暂无历史数据，请先使用/info命令记录数据")
    except (ValueError, PermissionError) as e:
        await ra_draw.finish(str(e))
    except Exception as e:
        await ra_draw.finish(f"生成图表失败：{str(e)}")

#v1.5
bind = on_command('bind')   
@bind.handle()
async def handle_bind(event: Event, message: Message = CommandArg()):
    name = str(message).strip()
    if name == '':
        await bind.finish("绑定不成功。绑定方式：/bind <查分器用户名>。例如：/bind ParrotNotFound")
    else:
        write_file(f"bind/{str(event.get_user_id())}.txt", name)
        await bind.finish(f"已将用户{str(event.get_user_id())}绑定至{name}")

#payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
#替换为
#payload = {'username': str(read_name(str(event.get_user_id()))),'b50':  True}
def read_name(qqid):
    try:
        name = read_file(f"bind/{qqid}.txt")
    except:
        name = str(qqid)
    return name
