# import os
# import re
# from functools import partial
# from typing import Optional, Union

# from openai import AsyncOpenAI, OpenAI
# from openai.types.chat import ChatCompletionUserMessageParam

# from qq_bot.basekit.config import settings
# from qq_bot.basekit.util import load_yaml


# class OpenAIBase:
#     def __init__(
#         self,
#         base_url: str,
#         api_key: str,
#         prompt_path: str,
#         default_model: str,
#         max_retries: int = 3,
#         **kwargs,
#     ) -> None:
#         assert os.path.isfile(prompt_path), f"Prompt {prompt_path} is not exist!"

#         self.api_key = api_key
#         self.base_url = base_url
#         self.prompt_path = prompt_path
#         self.default_model = default_model

#         self.raw_instruct: dict = load_yaml(prompt_path)
#         self.prompt: str = self.raw_instruct["instruct"]
#         # self.client = OpenAI(
#         #     base_url=settings.GPT_BASE_URL, api_key=settings.GPT_API_KEY, timeout=20
#         # )
#         self.async_client = AsyncOpenAI(
#             api_key=api_key,
#             base_url=base_url,
#             max_retries=max_retries,
#             timeout=20,
#             **kwargs,
#         )

#     def _set_prompt(self, input: dict, prompt: str | None = None) -> str:
#         def replacer(match, params: dict):
#             var_name = match.group(1)
#             return params.get(var_name, match.group(0))

#         def standardization(params: Union[dict, str]) -> dict:
#             params = {"data": params} if isinstance(input, str) else input
#             return {k: str(v) for k, v in params.items()}

#         params = standardization(input)
#         pattern = re.compile(r"\$\{(\w+)\}")
#         prompt = prompt if prompt else self.prompt
#         return pattern.sub(partial(replacer, params=params), prompt)

#     # def _inference(self, content: str, model: Optional[str] = None, **kwargs) -> str:
#     #     model = model or self.default_model

#     #     messages = [ChatCompletionUserMessageParam(content=content, role="user")]
#     #     completion = self.client.chat.completions.create(
#     #         messages=messages, model=model, **kwargs  # type: ignore
#     #     )
#     #     response = completion.choices[0].message.content
#     #     return response or "None"

#     async def _async_inference(self, content: str | list, model: Optional[str] = None, **kwargs) -> str:
#         model = model or self.default_model

#         if isinstance(content, str):
#             messages = [ChatCompletionUserMessageParam(content=content, role="user")]
#         else:
#             messages = content
#         completion = await self.async_client.chat.completions.create(messages=messages, model=model, **kwargs)

#         response = completion.choices[-1].message.content
#         return response or "None"
