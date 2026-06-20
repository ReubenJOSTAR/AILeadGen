from pydantic import BaseModel
from typing import List


class Message(BaseModel):
    role: str
    content: str


class ChatRequest(BaseModel):
    widget_id: str
    session_id: str
    message: str
    conversation_history: List[Message]


class ChatResponse(BaseModel):
    reply: str
    is_complete: bool
    extracted_data: dict
