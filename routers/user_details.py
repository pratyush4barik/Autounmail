from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import UserDetails
from database.schemas.user_details import UserProfileBase
from security.access_token import get_current_user

router = APIRouter(
    tags=["UserDetails"]
)

@router.post("/Userdetails")
def userDetails(
    data: UserProfileBase,
    db: Session = Depends(get_db)
):
    #1. check who is doing the request.
    user_id = get_current_user(data.access_token)

    #2. check that user having the details in the user table or not.
    existing_user = (
        db.query(UserDetails)
        .filter(UserDetails.user_id == user_id)
        .first()
    )

    # Update the existing row or create it when the user has no details yet.
    if existing_user:
        userdetails = existing_user
    else:
        userdetails = UserDetails(
            user_id = user_id,
        )
        db.add(userdetails)

    userdetails.name = data.name
    userdetails.college = data.college
    userdetails.degree = data.degree
    userdetails.branch = data.branch
    userdetails.resume_link = data.resume_link
    userdetails.github_link = data.github_link
    userdetails.linkedin_link = data.linkedin_link
    userdetails.drive_link = data.drive_link
    userdetails.roll_number = data.roll_number
    userdetails.year = data.year
    userdetails.cgpa = data.cgpa
    userdetails.skills = data.skills
    userdetails.projects = data.projects
    userdetails.research_interests = data.research_interests

    db.commit()
    db.refresh(userdetails)

    return {
        "message": "UserDetails updated." if existing_user else "UserDetails created."
    }