import aiohttp
import asyncio
from astrbot.api.event import filter, AstrMessageEvent
from astrbot.api.star import Context, Star, register
from astrbot.api.all import AstrBotConfig
from astrbot.api import logger


@register(
    "astrbot_plugin_163simple",
    "AstrBot Plugin Developer",
    "163简单网页内容获取插件",
    "1.0",
    ""
)
class Simple163Plugin(Star):
    def __init__(self, context: Context, config: AstrBotConfig):
        super().__init__(context)
        logger.info("163简单插件已初始化")

    @filter.command("163")
    async def handle_163_command(self, event: AstrMessageEvent):
        """处理163命令"""
        logger.info(f"收到163命令，来自群: {event.group_id}")

        try:
            # 发送请求
            async with aiohttp.ClientSession() as session:
                async with session.get("https://linluo.fuhongweb.cn/xiaohao/", timeout=10) as resp:
                    if resp.status == 200:
                        content = await resp.text()
                        # 简单截断避免消息过长
                        if len(content) > 400:
                            content = content[:400] + "..."
                        yield event.plain_result(f"获取到的内容:\n{content}")
                    else:
                        yield event.plain_result(f"请求失败，状态码: {resp.status}")
        except Exception as e:
            yield event.plain_result(f"请求出错: {str(e)}")