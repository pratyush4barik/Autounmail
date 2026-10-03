from pydantic import BaseModel, str

class ChangePassword(BaseModel):
    acess_token: str
    old_password: str
    new_password: str

class ChangePasswordResponse(BaseModel):
    message: str