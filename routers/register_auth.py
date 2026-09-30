from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import User, OTPVerification
from database.schemas.register_auth import UserCreate
from security.verification_id import generate_verification_id
from security.password import hash_password
from security.otp import (
    generate_otp,
    hash_otp,
    send_verification_email,
    get_otp_expiry
)


router = APIRouter(
    tags=["Register"]
)


@router.post("/register")
async def register(
    data: UserCreate,
    db: Session = Depends(get_db)
):
    return await register_user(data, db)


async def register_user(
    data: UserCreate,
    db: Session
):
    # 1. Check whether email already exists
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

    # 2. Hash password
    hashed_password = hash_password(
        data.password
    )

    # 3. Create user
    user = User(
        email=data.email,
        password_hash=hashed_password,
        auth_provider="Email",
        is_email_verified=False,
        is_active=True
    )

    db.add(user)
    db.commit()
    db.refresh(user)

    # 4. Generate verification data
    verification_id = generate_verification_id()
    otp = generate_otp()
    hashed_otp = hash_otp(otp)
    expiry_time = get_otp_expiry()

    # 5. Create OTP record
    otp_verification = OTPVerification(
        user_id=user.id,
        verification_id=verification_id,
        otp_hash=hashed_otp,
        purpose="Register",
        expires_at=expiry_time,
        attempts=0
    )

    db.add(otp_verification)
    db.commit()
    db.refresh(otp_verification)

    # 6. Send OTP email
    await send_verification_email(
        data.email,
        otp
    )

    # 7. Response to frontend
    return {
        "message": (
            "Registration successful. "
            "Please check your email for verification."
        ),
        "verification_id": verification_id
    }

