# app/api/v1/chat.py
from fastapi import APIRouter, HTTPException

# 注意这里：把 async_embed 也引入进来
from app.infra.llm import llm_client
from app.schemas import Result
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("", summary="基础对话接口")
async def chat_api(request: ChatRequest) -> Result[ChatResponse]:
    try:
        return await chat_service.chat(request)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM 调用失败: {str(e)}")


@router.get("/embed", summary="测试文本向量化")
async def test_embedding(text: str = "测试文本"):
    try:
        vector = await llm_client.async_embed(text)
        return {
            "text": text,
            "dimension": len(vector),  # 验证维度是否为我们配置的 4096
            "preview": vector[:5]  # 只预览前 5 个浮点数
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Embedding 调用失败: {str(e)}")
