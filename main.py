import aiohttp
import asyncio
from typing import Optional
from astrbot.api.message_components import Plain
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
        self.api_url = "https://linluo.fuhongweb.cn/xiaohao/"
        self.trigger_keyword = "163"
        logger.info(f"163简单插件已初始化，触发关键词: {self.trigger_keyword}")

    async def fetch_web_content(self) -> str:
        """获取网页内容"""
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36"
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(self.api_url, headers=headers, timeout=10) as response:
                    if response.status == 200:
                        text = await response.text()
                        # 简单清理文本
                        text = text.strip()
                        # 限制长度，避免消息过长
                        if len(text) > 500:
                            text = text[:500] + "...\n(内容过长，已截断)"
                        return text
                    else:
                        return f"请求失败，状态码: {response.status}"

        except asyncio.TimeoutError:
            return "请求超时"
        except Exception as e:
            return f"请求出错: {str(e)}"

    @filter.on_message()
    async def handle_163_message(self, event: AstrMessageEvent):
        """处理群聊中的163消息"""
        # 获取原始消息内容
        message = event.message_str.strip()

        # 只在群聊中响应
        if not hasattr(event, 'group_id') or not event.group_id:
            return

        # 检查消息是否完全匹配"163"
        if message != self.trigger_keyword:
            return

        logger.info(f"收到163请求，来自群: {event.group_id}")

        # 发送正在获取的提示
        yield event.plain_result("正在获取内容...")

        # 获取网页内容
        content = await self.fetch_web_content()

        # 构建响应
        response = f"获取到的内容:\n{content}"

        # 发送响应
        yield event.plain_result(response)