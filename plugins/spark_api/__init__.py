from nonebot import get_plugin_config
from nonebot.plugin import PluginMetadata

from .config import Config

__plugin_meta__ = PluginMetadata(
    name="spark_api",
    description="",
    usage="",
    config=Config,
)

config = get_plugin_config(Config)
# 在插件目录（如 plugins/spark_api）中的 __init__.py 文件
from nonebot import on_command
from nonebot.adapters import Event
from nonebot.rule import to_me
from nonebot.params import CommandArg
from nonebot.adapters.qq import Message, MessageSegment
#from nonebot.adapters.console import Message, MessageEvent
from nonebot.typing import T_State
from nonebot.log import logger
import aiohttp
import json
import hashlib
import hmac
import base64
from urllib.parse import urlparse
from datetime import datetime
from time import mktime
from wsgiref.handlers import format_date_time

# 配置项（在.env文件中配置）
SPARK_APP_ID = "2aa21cf6"
SPARK_API_KEY = "feedde8d6a2b04a06d04f13f02085737"
SPARK_API_SECRET = "NTMxYjdiMjIxY2UxNWE5MDU5MjYyM2U2"
SPARK_API_HOST = "ws://spark-api.xf-yun.com/v1/chat"

# 创建命令处理器
spark = on_command("ask", priority=5, block=True)

@spark.handle()
async def _(event: Event, message: Message = CommandArg()):
    question = message.extract_plain_text().strip()
    if not question:
        await spark.finish("请输入您的问题")
    
    try:
        response = await get_spark_response(question)
        await spark.send("请铜币为你解答："+ response)
    except Exception as e:
        logger.error(f"讯飞星火API调用失败: {str(e)}")
        await spark.finish("暂时无法回答，请稍后再试")

async def get_spark_response(question: str) -> str:
    # 构造请求URL
    url = create_spark_url()
    
    # 构造请求数据
    data = {
        "header": {
            "app_id": SPARK_APP_ID,
            "uid": "agbi"
        },
        "parameter": {
            "chat": {
                "domain": "general",
                "temperature": 0.5,
                "max_tokens": 2048
            }
        },
        "payload": {
            "message": {
                "text": [{"role": "user", "content": question}]
            }
        }
    }

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(url) as ws:
            await ws.send_str(json.dumps(data))
            result = ""
            
            async for msg in ws:
                if msg.type == aiohttp.WSMsgType.TEXT:
                    response = json.loads(msg.data)
                    if response["header"]["code"] != 0:
                        raise Exception(f"API Error: {response['header']['message']}")
                    
                    # 拼接响应内容
                    choices = response["payload"]["choices"]
                    result += choices["text"][0]["content"]
                    
                    # 判断是否结束
                    if choices["status"] == 2:
                        break
                elif msg.type == aiohttp.WSMsgType.ERROR:
                    raise Exception("WebSocket connection closed with error")
    
    return result

def create_spark_url() -> str:
    # 生成鉴权URL
    host = urlparse(SPARK_API_HOST).netloc
    path = urlparse(SPARK_API_HOST).path
    
    # 生成RFC1123格式时间戳
    now = datetime.now()
    date = format_date_time(mktime(now.timetuple()))
    
    # 拼接签名字符串
    signature_origin = f"host: {host}\ndate: {date}\nGET {path} HTTP/1.1"
    
    # 进行hmac-sha256加密
    signature_sha = hmac.new(SPARK_API_SECRET.encode('utf-8'),
                            signature_origin.encode('utf-8'),
                            digestmod=hashlib.sha256).digest()
    
    signature_sha_base64 = base64.b64encode(signature_sha).decode(encoding='utf-8')
    
    # 构造授权参数
    authorization_origin = f'api_key="{SPARK_API_KEY}", algorithm="hmac-sha256", headers="host date request-line", signature="{signature_sha_base64}"'
    authorization = base64.b64encode(authorization_origin.encode('utf-8')).decode(encoding='utf-8')
    
    # 构造请求URL
    return f"{SPARK_API_HOST}?authorization={authorization}&date={date}&host={host}"


