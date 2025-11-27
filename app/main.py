import time
from fastapi import FastAPI
from pydantic import BaseModel

from .model import CodeFixModel


app = FastAPI()
model = CodeFixModel()


class FixRequest(BaseModel):
    language: str
    cwe: str
    code: str
    vulnerability_type: str


@app.post("/local_fix")
def local_fix(req: FixRequest):
    start = time.time()

    (
        fixed_code,
        explanation,
        diff,
        model_used,
        input_tokens,
        output_tokens,
    ) = model.generate_fix(req.vulnerability_type, req.code)

    latency_ms = (time.time() - start) * 1000.0

    return {
        "fixed_code": fixed_code,
        "explanation": explanation,
        "diff": diff,
        "model_used": model_used,
        "token_usage": {
            "input_tokens": input_tokens,
            "output_tokens": output_tokens,
        },
        "latency_ms": latency_ms,
    }
