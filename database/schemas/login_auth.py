from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field, model_validator

class MessageResponse(BaseModel):
    message: str