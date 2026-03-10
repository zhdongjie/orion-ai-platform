# app/infra/llm/message_adapter.py
from typing import List

from langchain_core.messages import (
    BaseMessage,
    HumanMessage,
    AIMessage,
    SystemMessage,
    ToolMessage,
)

from app.schemas.message import Message


def lc_to_openai(messages: List[BaseMessage]) -> List[dict]:
    result = []

    for msg in messages:
        if isinstance(msg, HumanMessage):
            role = "user"
        elif isinstance(msg, AIMessage):
            role = "assistant"
        elif isinstance(msg, SystemMessage):
            role = "system"
        elif isinstance(msg, ToolMessage):
            role = "tool"
        else:
            role = "user"
        result.append({
            "role": role,
            "content": msg.content
        })

    return result


def schema_to_lc(messages: List[Message]) -> List[BaseMessage]:
    """
    Schema Message → LangChain Message
    """

    lc_messages = []

    for msg in messages:

        if msg.role == "user":
            lc_messages.append(HumanMessage(content=msg.content))

        elif msg.role == "assistant":
            lc_messages.append(AIMessage(content=msg.content))

        elif msg.role == "system":
            lc_messages.append(SystemMessage(content=msg.content))

    return lc_messages
