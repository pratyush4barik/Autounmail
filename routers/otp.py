from fastapi import APIRouter, Depends, HTTPException
from datetime import datetime, timedelta
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import OTPVerification, User
from database.schemas.otp import Resend,Verify
from security.otp import (
    generate_otp,
    hash_otp,
    send_verification_email,
    get_otp_expiry,
    verify_otp
)


router = APIRouter(
    tags=["OTP"]
)


@router.post("/otp-resend")
async def resend_otp(
    data: Resend,
    db: Session = Depends(get_db)
):

    # 1. Find verification record
    verification = (
        db.query(OTPVerification)
        .filter(OTPVerification.verification_id == data.verification_id)
        .first()
    )

    if verification is None:
        raise HTTPException(
            status_code=404,
            detail="Verification ID not found."
        )

    # 2. Find user using user_id
    user = (
        db.query(User)
        .filter(User.id == verification.user_id)
        .first()
    )

    if user is None:
        raise HTTPException(
            status_code=404,
            detail="User not found."
        )

    # 3. Don't allow resend if already verified
    if verification.verified:
        raise HTTPException(
            status_code=400,
            detail="Email is already verified."
        )

    # 4. Generate new OTP
    new_otp = generate_otp()

    # 5. Hash OTP
    hashed_otp = hash_otp(new_otp)

    # 6. Generate new expiry time
    expiry_time = get_otp_expiry()

    # 7. Update existing verification record
    verification.otp_hash = hashed_otp
    verification.expires_at = expiry_time
    verification.attempts = 0
    verification.locked = False

    db.commit()
    db.refresh(verification)

    # 8. Send new OTP
    await send_verification_email(
        user.email,
        new_otp
    )

    # 9. Response
    return {
        "message": "New OTP has been sent to your email."
    }

@router.post("/otp-verify")
def verify_otp(
    data: Verify,
    db: Session = Depends(get_db)
):
    # Find the row using verification_id
    verification=(
        db.query(OTPVerification)
        .filter(OTPVerification.verification_id == data.verification_id)
        .first()
        )

    #If not found raise an error and exit.
    if verification is None:
        raise HTTPException(
            status_code=400,
            detail="Verification id not found."
        )

    #Find user row using the user.id present in the verification row the attached user.
    user=(
        db.query(User)
        .filter(User.id == verification.user_id)
        .first()
        )
    
    #If not found raise an error and exit.
    if user is None:
        raise HTTPException(
            status_code=400,
            detail="User not found."
        )

    #Check it is already verified or not.
    if user.is_email_verified is True:
        raise HTTPException(
            status_code=400,
            detail="Email is already Verified."
        )

    #Check it is already expired or not.
    if verification.expires_at < datetime.utcnow():
        raise HTTPException(
            status_code=400,
            detail="Otp is Expired."
        )

    #Check it is locked or not.
    if verification.locked is True:
        raise HTTPException(
            status_code=400,
            detail="Otp is locked"
        )

    #Verifies the OTP.
    otp_verification = verify_otp(
        data.otp,
        verification.otp_hash
    )

    #If it has reached maximum attempts then lock it.
    if verification.attempts == verification.max_attempts:
        verification.locked = True

    #For each attempt increase it by 1.
    verification.attempts=+1

    #Raise an error if it is an Incorrect OTP.
    if otp_verification is False:
        raise HTTPException(
            status_code=400,
            detail="Incorrect OTP"
        )

    #Updates the is_email_verified at user row and the verified at verification row marks as TRUE. 
    user.is_email_verified = True
    verification.verified = True

    db.commit()
    db.refresh(user)
    db.refresh(verification)  

    return {
        "message": "Your email is Verified."
    }
    
    