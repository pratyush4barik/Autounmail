from pydantic import BaseModel, Field, Str, configDict, model_validator
from datetime import datetime

class FilterChats(BaseModel):
    access_token: str
    title : str
    created_at: datetime

class messageResponse(BaseModel):
    message: str

    model_config = configDict(from_attributes=True)

