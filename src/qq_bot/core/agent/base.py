from ncatbot.plugin import BasePlugin
from ncatbot.core import BotClient, BotAPI
from qq_bot.core.res_manager.news_capturer import NewsLoader
from qq_bot.core.llm_manager.llm_registrar import LLMRegistrar
from qq_bot.core.tool_manager.base import ToolRegistrarBase


class AgentBase(BasePlugin):
    def __init__(self, **kwargs):
        self.bot: BotClient | None = None
        self.tools: ToolRegistrarBase | None = None

        super().__init__(**kwargs)

    async def on_load(self):
        pass

    def register_handlers(self):
        pass

    def run(self):
        pass
