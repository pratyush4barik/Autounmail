from fastapi import HTTPException
from datetime import datetime, timezone, timedelta
from jose import jwt, JWTError
import os
from dotenv import load_dotenv

load_dotenv()
SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")

def create_refresh_token(user_id: int):

    expire = datetime.now(timezone.utc) + timedelta(days=15)

    payload = {
        "sub": user_id,
        "exp": expire,
        "type": "refresh"
    }

    return jwt.encode(
        payload,
        SECRET_KEY,
        algorithm=ALGORITHM
    )

if __name__ == "__main__":
    refresh = create_refresh_token(12)
    print(refresh)