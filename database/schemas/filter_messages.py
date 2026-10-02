from pydantic import BaseModel, Field, str, configDict
from uuid import UUID
from database.schemas.message_role import MessageRole
from datetime import datetime

class FilterMessages(BaseModel):
    access_token: str
    content: str


class EmailMessagesResponse(BaseModel):
    id: UUID
    chat_id: UUID
    role: MessageRole
    content: str
    created_at: datetime

    model_config = configDict(from_attributes=True)