from pydantic import BaseModel, str
from datetime import datetime

class EmailChats(BaseModel):
    access_token: str
    title: str
    created_at: datetime