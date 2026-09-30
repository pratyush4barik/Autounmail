from fastapi import APIRouter, Depends, HTTPException
from database.schemas.change_password import ChangePassword
from sqlalchemy.orm import Session
from database.database import get_db
from database.models import Session

router=APIRouter(
    tags=["Change-Password"]
)

@router.post("/change-password")
def change_password(
    data: ChangePassword,
    db: Session = Depends(get_db)
):
    
    # Find the user via the acess token.
    access_token =(
        db.querry(Session)
        # .filter(Session.token_hash == )
    )
    
