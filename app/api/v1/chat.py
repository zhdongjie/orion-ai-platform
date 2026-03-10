# app/api/v1/chat.py
from fastapi import APIRouter

from app.infra.llm import llm_client
from app.schemas import Result
from app.schemas.chat import ChatRequest, ChatResponse
from app.services.chat_service import chat_service

router = APIRouter()


@router.post("", summary="基础对话接口", response_model=Result[ChatResponse])
async def chat_api(request: ChatRequest) -> Result[ChatResponse]:
    return await chat_service.chat(request)


@router.get("/embed", summary="测试文本向量化", response_model=Result)
async def test_embedding(text: str = "测试文本") -> Result:
    vector = await llm_client.async_embed(text)

    return Result.success(
        {
            "text": text,
            "dimension": len(vector),
            "preview": vector[:5]
        }
    )
