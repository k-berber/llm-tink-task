from fastapi import FastAPI
import uvicorn

from utils import MessageInfo


app = FastAPI()


@app.get("/health")
async def check_health() -> dict:
    return {"health": "ok"}


@app.get("/message")
async def message(message_info: MessageInfo) -> dict:
    return {"health": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
