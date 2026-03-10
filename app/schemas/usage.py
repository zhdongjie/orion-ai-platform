# app/schemas/usage.py
from typing import Optional

from pydantic import Field

from app.schemas import BaseSchema


class Usage(BaseSchema):

    prompt_tokens: Optional[int] = Field(
        default=None,
        description="Prompt Token"
    )

    completion_tokens: Optional[int] = Field(
        default=None,
        description="Completion Token"
    )

    total_tokens: Optional[int] = Field(
        default=None,
        description="总 Token"
    )