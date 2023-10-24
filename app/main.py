from fastapi import FastAPI
import uvicorn

from utils import MessageInfo, get_answer_from_llm


app = FastAPI()


@app.get("/health")
async def check_health() -> dict:
    return {"health": "ok"}


@app.post("/message")
async def message(message_info: MessageInfo) -> dict:
    return {"answer": get_answer_from_llm(message_info)}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
