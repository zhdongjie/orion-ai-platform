# app/infra/llm/zhipu_client.py
from openai import AsyncOpenAI

from app.core.config import settings

# 依然使用高并发的 AsyncOpenAI 客户端，只是传参换成了你的专属配置
client = AsyncOpenAI(
    api_key=settings.ZHIPU_API_KEY,
    base_url=settings.ZHIPU_API_BASE
)


async def async_chat(query: str) -> str:
    """调用大模型的底层函数"""
    response = await client.chat.completions.create(
        model=settings.ZHIPU_MODEL_GLM,  # 使用 glm-4-flash
        messages=[
            {"role": "system", "content": "你是一个专业的企业级AI助手。"},
            {"role": "user", "content": query}
        ],
        temperature=0.7
    )
    return response.choices[0].message.content


# 💡 提前写好 Embedding 函数，为 Phase 2 知识库做准备！
async def async_embed(text: str) -> list[float]:
    """生成文本向量的底层函数"""
    response = await client.embeddings.create(
        model=settings.ZHIPU_MODEL_EMBEDDING,  # 使用 glm-embedding-6b
        input=text
    )
    return response.data[0].embedding
