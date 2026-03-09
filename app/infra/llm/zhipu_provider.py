from openai import AsyncOpenAI

from app.core.config import settings
from app.infra.llm.base import BaseLLMProvider


class ZhipuProvider(BaseLLMProvider):
    def __init__(self):
        self.client = AsyncOpenAI(
            api_key=settings.ZHIPU_API_KEY,
            base_url=settings.ZHIPU_API_BASE
        )
        self.model = settings.ZHIPU_MODEL_GLM
        self.embed_model = settings.ZHIPU_MODEL_EMBEDDING

    async def async_chat(self, query: str) -> str:
        response = await self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": query}]
        )
        return response.choices[0].message.content

    async def async_embed(self, text: str) -> list[float]:
        response = await self.client.embeddings.create(
            model=self.embed_model,
            input=text
        )
        return response.data[0].embedding
