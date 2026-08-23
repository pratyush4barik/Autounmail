from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User
from database.schemas.register_auth import UserCreate

router = APIRouter(tags=["Register"])
from security.password import hash_password

@router.post("/register")
def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    return register_user(data, db)


def register_user(
    data: UserCreate,
    db: Session
):
    existing_user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    if existing_user:
        raise HTTPException(
            status_code=400,
            detail="Email already registered"
        )

    user = User(
        email=data.email,
        password_hash=hash_password(data.password),
        auth_provider="Email",
        is_email_verified=False,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    return {
        "message": "Registration successful"
    }