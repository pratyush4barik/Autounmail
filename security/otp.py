import os
import secrets
from datetime import datetime, timedelta
from dotenv import load_dotenv
import resend
from pwdlib import PasswordHash
import asyncio
load_dotenv()

password_hash = PasswordHash.recommended()

resend.api_key = os.getenv("RESEND_API_KEY")

FROM_EMAIL = os.getenv(
    "RESEND_FROM_EMAIL"
)


def generate_otp() -> str:
    return f"{secrets.randbelow(1_000_000):06d}"



def hash_otp(otp: str) -> str:
    return password_hash.hash(otp)


def verify_otp(
    otp: str,
    otp_hash: str
) -> bool:
    return password_hash.verify(
        otp,
        otp_hash
    )


def get_otp_expiry() -> datetime:
    return datetime.utcnow() + timedelta(
        minutes=10
    )


async def send_verification_email(
    email: str,
    otp: str
):
    params: resend.Emails.SendParams = {
        "from": FROM_EMAIL,
        "to": [email],
        "subject": "Verify your email",
        "html": f"""
            <h2>Email Verification</h2>

            <p>Your verification code is:</p>

            <h1>{otp}</h1>

            <p>
                This code expires in 10 minutes.
            </p>

            <p>
                If you did not create this account,
                you can ignore this email.
            </p>
        """
    }

    return await resend.Emails.send_async(params)


#this is for testing purposes only, you can remove it in production

if __name__ == "__main__":
    # Example usage
    print("API key loaded:", bool(resend.api_key))
    generated_otp = generate_otp()
    print(f"Generated OTP: {generated_otp}")
    hashed_otp = hash_otp(generated_otp)
    print(f"Hashed OTP: {hashed_otp}")
    email = "vex7208@gmail.com"
    asyncio.run(send_verification_email(email, generated_otp))
    expiry_time = get_otp_expiry()
    print(f"OTP expires at: {expiry_time}")
    manual_otp = input("Enter the OTP you received: ")
    verified = verify_otp(manual_otp, hashed_otp)
    print(f"OTP Verified: {verified}")