from pydantic import BaseModel

class Resend(BaseModel):
    verification_id: str

class Verify(BaseModel):
    verification_id: str
    otp: str