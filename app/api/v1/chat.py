# app/api/v1/chat.py
from fastapi import APIRouter, HTTPException

# 注意这里：把 async_embed 也引入进来
from app.infra.llm.zhipu_client import async_chat, async_embed

router = APIRouter()


@router.post("", summary="基础对话接口")
async def chat_api(query: str):
    try:
        answer = await async_chat(query)
        return answer
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {str(e)}")


@router.get("/embed", summary="测试文本向量化")
async def test_embedding(text: str = "测试文本"):
    try:
        vector = await async_embed(text)
        return {
            "text": text,
            "dimension": len(vector),  # 验证维度是否为我们配置的 4096
            "preview": vector[:5]  # 只预览前 5 个浮点数
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding 调用失败: {str(e)}")
