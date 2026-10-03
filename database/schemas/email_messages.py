from pydantic import BaseModel, Field, str, ConfigDict
from uuid import UUID
from database.schemas.message_role import MessageRole
from datetime import datetime

class EmailMessages(BaseModel):
    access_token: str
    content: str


class FilterMessagesResponse(BaseModel):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    model_config = ConfigDict(from_attributes=True)