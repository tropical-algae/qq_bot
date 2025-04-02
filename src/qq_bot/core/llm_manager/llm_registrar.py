import os
from qq_bot.utils.config import settings
from qq_bot.utils.logging import logger
from qq_bot.core.llm_manager.llms.base import OpenAIBase
import qq_bot.core.llm_manager.llms as bot_llms
from qq_bot.utils.util import import_all_modules_from_package


class LLMRegistrar:
    def __init__(self, prompt_root: str):
        self.prompt_root = prompt_root
        self.model_services: dict[str, OpenAIBase] = {}
        self._load_model_services()

    def _load_model_services(self) -> None:
        import_all_modules_from_package(bot_llms)
        
        model_services = OpenAIBase.__subclasses__()
        logger.info("正在注册模型服务")
        for model_service in model_services:
            tag = model_service.__model_tag__
            prompt_path = os.path.join(self.prompt_root, f"{tag}.yaml")
            self.model_services[tag] = model_service(
                base_url=settings.GPT_BASE_URL,
                api_key=settings.GPT_API_KEY,
                prompt_path=prompt_path,
            )
            if self.model_services[tag].is_activate:
                logger.info(f"已注册模型：{tag}")
            else:
                logger.warning(f"已注册模型：{tag} [未激活 模型不可用]")
    
    def get(self, model_tag: str) -> OpenAIBase | None:
        return self.model_services.get(model_tag, None)


llm_registrar = LLMRegistrar(prompt_root=settings.LOCAL_PROMPT_ROOT)


# a = [
#     "[AAA][2025-3-13 13:12:30]:明天去吃饭？",
#     "[BBB][2025-3-13 13:12:30]:我不去，你们去吧",
#     "[DDD][2025-3-13 13:12:30]:不是哥们",
#     "[CCC][2025-3-13 13:12:30]:你们谁玩过沙滩排球",
#     "[EEE][2025-3-13 13:12:30]:我去",
#     "[AAA][2025-3-13 13:12:30]:没玩过捏，我只玩过生与死",
# ]

# b = asyncio.run(llm_registrar.get(settings.RELATION_EXTOR_LLM_CONFIG_NAME).run(message=a))
# print(b)
