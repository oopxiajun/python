from langchain_core.language_models.llms import BaseLLM
from langchain_core.outputs import Generation, LLMResult
from pydantic.v1 import Field, validator
from typing import Any, Dict, List, Optional, AsyncIterator
import requests
import os

class DeepSeekLLM(BaseLLM):
    api_key: str = Field(alias="api_key")
    model: str = "deepseek-chat"
    temperature: float = 0.7
    max_tokens: int = 1000

    # 必须实现的抽象方法
    def _generate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        generations = []
        for prompt in prompts:
            response = self._call_api(prompt)
            generations.append([Generation(text=response)])
        return LLMResult(generations=generations)

    async def _agenerate(
        self,
        prompts: List[str],
        stop: Optional[List[str]] = None,
        **kwargs: Any,
    ) -> LLMResult:
        # 异步实现（可选）
        return self._generate(prompts, stop, **kwargs)

    def _call_api(self, prompt: str) -> str:
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        payload = {
            "messages": [{"role": "user", "content": prompt}],
            "model": self.model,
            "temperature": self.temperature,
            "max_tokens": self.max_tokens
        }
        response = requests.post(
            "https://api.deepseek.com/v1/chat/completions",
            headers=headers,
            json=payload
        )
        if response.status_code == 200:
            return response.json()["choices"][0]["message"]["content"]
        else:
            raise ValueError(f"API Error: {response.text}")

    @property
    def _llm_type(self) -> str:
        return "deepseek"