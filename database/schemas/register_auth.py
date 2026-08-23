from pydantic import BaseModel, EmailStr, ConfigDict, field_validator, Field, model_validator

class MessageResponse(BaseModel):
    message: str

class UserCreate(BaseModel):
    email: EmailStr
    password: str = Field(
        min_length=8,
        max_length=128,
        pattern =r"[a-zA-Z0-9_!@#$&*%]+$"
        )
    confirm_password: str

    @model_validator(mode="after")
    def password_match(self):
        if self.password != self.confirm_password:
            raise ValueError("Passwords do not match")
        return self

# r = regex engine
# +  = one or more
# *  = zero or more
# ?  = zero or one
