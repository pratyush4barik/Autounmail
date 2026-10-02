from pydantic import BaseModel, Field, str, configDict
from uuid import UUID
from datetime import datetime

class ApiKeys(BaseModel):
    access_token: str
    api_key: str

class ApiKeysResponse(BaseModel):
    id: UUID
    access_token: str
    api_key: str
    created_at: datetime
    updated_at: datetime

    model_config = configDict(from_attributes=True)

    