from pydantic import BaseModel


class MessageInfo(BaseModel):
    message: str
    user_id: str


class Loader:
    def __init__(self):
        pass