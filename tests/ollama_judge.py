import json
import re
from typing import Optional, Type

import ollama
from pydantic import BaseModel
from deepeval.models.base_model import DeepEvalBaseLLM

# usado como wapper para o deepeval, que naturalmente nao suporta os modelos ollmaa como str
class OllamaJudge(DeepEvalBaseLLM):
    """Adapta o Ollama à interface DeepEvalBaseLLM para uso como juiz nas métricas."""

    def __init__(self, model: str, host: str):
        self.model = model
        self.host = host
        self._client = ollama.Client(host=host)

    def load_model(self):
        return self.model

    def generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None):
        response = self._client.chat(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            format=schema.model_json_schema() if schema else None,
        )
        content = response["message"]["content"]
        if schema is None:
            return content
        try:
            return schema(**json.loads(content))
        except Exception:
            match = re.search(r"\{.*\}", content, re.DOTALL)
            if match:
                return schema(**json.loads(match.group()))
            raise

    async def a_generate(self, prompt: str, schema: Optional[Type[BaseModel]] = None):
        return self.generate(prompt, schema)

    def get_model_name(self) -> str:
        return f"ollama/{self.model}"
