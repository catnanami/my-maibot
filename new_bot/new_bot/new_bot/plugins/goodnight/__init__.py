from nonebot import get_driver

from .config import Config
from nonebot.plugin import on_keyword
from nonebot.adapters.onebot.v11 import Bot, Event
from nonebot.adapters.onebot.v11.message import Message
global_config = get_driver().config
config = Config.parse_obj(global_config)

goodnight=on_keyword(['晚安'],priority=20)

@goodnight.handle()
async def goodnight_function():
    await goodnight.finish(Message('晚安喵~mua~'))

