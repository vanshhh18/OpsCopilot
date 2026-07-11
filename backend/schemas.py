from pydantic import BaseModel


class ChatRequest(BaseModel):
    session_id: str
    message: str


class ConfirmRequest(BaseModel):
    action_id: int


class RejectRequest(BaseModel):
    action_id: int