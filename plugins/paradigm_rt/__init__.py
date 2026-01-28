from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="paradigm_rt",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)

from nonebot.rule import to_me, startswith
from nonebot.plugin import on_command,on_message
from nonebot.params import CommandArg, EventMessage
from nonebot.adapters.qq import Message, MessageSegment
#from nonebot.adapters.console import Message, MessageEvent
from nonebot.adapters import Event
from nonebot.log import logger

def calculate_single_rating(chart_difficulty, score):
    # 定义评级系数字典
    rating_coefficients = {
        '∞': 9,
        'AAA+': 8,
        'AAA': 7,
        'AA+': 6,
        'AA': 5,
        'A+': 4,
        'A': 3,
        'B': 0,
        'C': 0,
        'D': 0
    }
    
    # 根据分数确定评级
    if score >= 1009000 and score <= 1010000:
        rating = '∞+'
    elif score >= 1000000:
        rating = '∞'
    elif score >= 990000:
        rating = 'AAA+'
    elif score >= 980000:
        rating = 'AAA'
    elif score >= 970000:
        rating = 'AA+'
    elif score >= 950000:
        rating = 'AA'
    elif score >= 930000:
        rating = 'A+'
    elif score >= 900000:
        rating = 'A'
    elif score >= 850000:
        rating = 'B'
    elif score >= 800000:
        rating = 'C'
    elif score >= 0:
        rating = 'D'
    else:
        raise ValueError("Invalid score")
    
    # 计算单曲Rating
    if rating == '∞+':
        single_rating = 10 * (chart_difficulty + 0.7 + 0.3 * ((score - 1009000) / 1000) ** 1.35)
    elif rating == '∞':
        single_rating = 10 * (chart_difficulty + 2/3 * ((score - 1000000) / 10000))
    else:
        single_rating = 10 * (chart_difficulty * (score / 1000000) ** 1.5 - 0.9) + rating_coefficients[rating]
    
    return round(single_rating, 4)

pdm = on_command("pdm",aliases={"pdg","pd"})

@pdm.handle()
async def _(event: Event, message: Message = CommandArg()):
    try:
        args = str(message).split(' ')
        if len(args) != 2:
            #await pdm.finish("使用方式：/pdm 定数 分数")
            raise
        else:
            ds = float(args[0])
            score = int(args[1])
            rt = calculate_single_rating(ds,score)
            await pdm.send(f"谱面定数：{ds}\n分数：{score}\n单曲Rating：{rt}")
    except Exception as e:
        print(e)
        await pdm.finish("出现了错误！使用方式：/pdm 定数 分数")