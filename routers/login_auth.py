from fastapi import APIRouter, Depends, HTTPException
from database.schemas.login_auth import LoginResponse
from database.database import get_db
from sqlalchemy.orm import Session
from database.models import User,OTPVerification
from security.password import verify_password
from security.otp import (
    get_otp_expiry,
    generate_otp, 
    hash_otp, 
    send_verification_email
)
from security.verification_id import generate_verification_id

router = APIRouter(
    tags=["login"]
)

@router.post("/login")
async def login(
    data: LoginResponse,
    db: Session = Depends(get_db)
):
    # Find the user via Email.
    user = (
        db.query(User)
        .filter(User.email == data.email)
        .first()
    )

    #If not found raise an error and exit.
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="Email not found."
        )

    #verify the password from the db user row.
    if verify_password(
        data.password,
        user.password_hash
        ) is False:
        raise HTTPException(
            status_code=400,
            detail="Password is incorrect."
        )
    

    #check if the email is verified or not.
    if user.is_email_verified is False:
        otp_verification=(
            db.query(OTPVerification)
            .filter(user.id == OTPVerification.user_id)
            .first()
        )
        if otp_verification:
            db.delete(otp_verification)
            db.commit()

        verification_id = await login_otp_flow(
            user=user,
            email=data.email,
            db=db
            )

    #further acess and refresh token to be added.
    return {
        "message": verification_id
    }


async def login_otp_flow(user, email, db):
    #Generates the verification id.
    verification_id = generate_verification_id()
    #Generates the otp.
    otp = generate_otp()
    #hashes the otp.
    hashed_otp = hash_otp(otp)
    expiry_time = get_otp_expiry()

    otp_verification = OTPVerification(
        user_id=user.id,
        verification_id=verification_id,
        otp_hash=hashed_otp,
        purpose="Login",
        expires_at=expiry_time,
        attempts=0
    )

    db.add(otp_verification)
    db.commit()
    db.refresh(otp_verification)

    await send_verification_email(
        email,
        otp
    )

    return verification_id

    





    