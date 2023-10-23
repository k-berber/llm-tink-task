from fastapi import FastAPI
import uvicorn


app = FastAPI()


@app.get("/health")
async def check_health():
    return {"health": "ok"}


@app.get("/message")
async def message(message, user_id):
    return {"health": "ok"}


if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8080)
