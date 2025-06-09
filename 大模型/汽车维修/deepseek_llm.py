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
        print("_generate:")
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
        try:
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
            #将输入 输出都保存到文件中 
            import json
            # 添加一个分隔符 没有  json.txt 就创建
            with open("json.txt", "a", encoding="utf-8") as f:
                f.write("############################################################\n")
            with open("json.txt", "a", encoding="utf-8") as f:
                json.dump(payload, f, ensure_ascii=False, indent=4)
            
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=payload,
                timeout=30
            )
            with open("json.txt", "a", encoding="utf-8") as f:
                json.dump(response.json(), f, ensure_ascii=False, indent=4)
            # 增加响应内容验证
            if not response.text.strip():
                raise ValueError("API返回空响应")
                
            try:
                data = response.json()
            except json.JSONDecodeError:
                # 尝试提取可能的JSON片段
                import re
                json_match = re.search(r'```json\n({.*?})\n```', response.text, re.DOTALL)
                if json_match:
                    data = json.loads(json_match.group(1))
                else:
                    raise ValueError(f"无法解析API响应: {response.text[:200]}...")

            # 验证关键字段
            if not data.get("choices") or not isinstance(data["choices"], list):
                raise ValueError("API返回格式异常，缺少choices字段")
                
            content = data["choices"][0]["message"]["content"]
            
            # 清理响应内容（去除可能的Markdown标记）
            if content.startswith("```json"):
                content = content[7:-3].strip()
            return content
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"API请求失败: {str(e)}")
        except Exception as e:
            raise ValueError(f"处理API响应时出错: {str(e)}")
        
    @property
    def _llm_type(self) -> str:
        return "deepseek"