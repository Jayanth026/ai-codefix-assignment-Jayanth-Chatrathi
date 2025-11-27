from pydantic import BaseModel, Field
from typing import Dict


class CodeFixRequest(BaseModel):
    language: str = Field(..., example="java")
    cwe: str = Field(..., example="CWE-89")
    code: str = Field(..., example="String query = \"SELECT * FROM users WHERE id=\" + userId;")


class TokenUsage(BaseModel):
    input_tokens: int
    output_tokens: int


class CodeFixResponse(BaseModel):
    fixed_code: str
    diff: str
    explanation: str
    model_used: str
    token_usage: TokenUsage
    latency_ms: float