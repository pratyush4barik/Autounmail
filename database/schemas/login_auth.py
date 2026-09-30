from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field, model_validator

class MessageResponse(BaseModel):
    message: str

class LoginResponse(BaseModel):
    email: EmailStr
    password: str