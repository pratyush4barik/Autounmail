from typing import Optional
from pydantic import BaseModel, ConfigDict

class UserProfileBase(BaseModel):
    access_token: str
    name: Optional[str] = None
    college: Optional[str] = None
    degree: Optional[str] = None
    branch: Optional[str] = None
    resume_link: Optional[str] = None
    github_link: Optional[str] = None
    drive_link: Optional[str] = None
    linkedin_link: Optional[str] = None
    roll_number:Optional[str] = None
    year: Optional[str] = None
    cgpa: Optional[float] = None
    skills: Optional[str] = None
    projects: Optional[str] = None
    research_interests: Optional[str] = None

    model_config= ConfigDict(from_attributes=True)