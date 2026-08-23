from sqlalchemy import (
    Column,
    Integer,
    String,
    Float,
    Boolean,
    Text,
    DateTime,
    ForeignKey
)
from datetime import datetime
from database.database import Base
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func

# 7. Encrypt Google OAuth tokens

class User(Base):
    __tablename__ = "users"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    password_hash = Column(
        String,
        nullable=True
    )
    auth_provider = Column(
        String,
        nullable=False,
    )
    google_id = Column(
        String,
        unique=True,
        nullable=True,
        index=True
    )
    is_email_verified = Column(
        Boolean,
        default=False
    )
    is_active = Column(
        Boolean,
        default=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    gmail_accounts = relationship(
        "GmailAccounts",
        back_populates="user",
    )
    oauth_states = relationship(
        "OAuthState",
        back_populates="user"
    )
    otp_verifications = relationship(
        "OTPVerification",
        back_populates="user"
    )
    sessions = relationship(
        "Session",
        back_populates="user"
    )
    user_details = relationship(
        "UserDetails",
        back_populates="user"
    )
    filter_chats = relationship(
        "FilterChat",
        back_populates="user"
    )
    email_chats = relationship(
        "EmailChat",
        back_populates="user"
    )
    user_api_keys = relationship(
        "UserAPIKeys",
        back_populates="user"
    )

class OTPVerification(Base):
    __tablename__ = "otp_verifications"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    verification_id = Column(
        String,
        unique=True,
        index=True,
        nullable=False
    )
    otp_hash = Column(
        String,
        nullable=False
    )
    purpose = Column(
        String,
        nullable=False
    )
    expires_at = Column(
        DateTime,
        nullable=False
    )
    attempts = Column(
        Integer,
        nullable=False,
        default=0
    )
    max_attempts = Column(
        Integer,
        nullable=False,
        default=5
    )
    locked = Column(
        Boolean,
        nullable=False,
        default=False
    )
    verified = Column(
        Boolean,
        nullable=False,
        default=False
    )
    created_at = Column(
        DateTime,
        nullable=False,
        default=datetime.utcnow
    )
    user = relationship(
        "User",
        back_populates="otp_verifications"
    )

class Session(Base):
    __tablename__ = "sessions"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    token_type = Column(
        String,
        nullable=False
    )
    token_hash = Column(
        String,
        nullable=False
    )
    expires_at = Column(
        DateTime,
        nullable=False
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    revoked = Column(
        Boolean,
        nullable=False,
        default=False
    )
    revoked_at = Column(
        DateTime,
        nullable=True
    )
    password_token_used = Column(
        Boolean,
        nullable=True
    )
    user = relationship(
        "User",
        back_populates="sessions"
    )

class UserDetails(Base):
    __tablename__ = "user_details"

    id = Column(
        Integer,
        primary_key=True, 
        index=True
        )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True,
        unique=True
    )
    name = Column(
        String, 
        nullable=True
        )
    college = Column(
        String, 
        nullable=True
        )
    degree = Column(
        String, 
        nullable=True
        )
    branch = Column(
        String,
        nullable=True
        )
    resume_link = Column(
        String, 
        nullable=True
        )
    github_link = Column(
        String, 
        nullable=True
        )
    linkedin_link = Column(
        String, 
        nullable=True
        )
    drive_link = Column(
        String, 
        nullable=True
        )
    roll_number = Column(
        String, 
        nullable=True
        )
    year = Column(
        String, 
        nullable=True
        )
    cgpa = Column(
        Float, 
        nullable=True
        )
    skills = Column(
        String, 
        nullable=True
        )
    projects = Column(
        String, 
        nullable=True
        )
    research_interests = Column(
        String, 
        nullable=True
        )
    user = relationship(
        "User",
        back_populates="user_details"
        )

class FilterChat(Base):
    __tablename__ = "filter_chats"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    user_id = Column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False,
        index=True
        )
    title = Column(
        String(255), 
        nullable=False
        )
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
        )
    user = relationship(
        "User",
        back_populates="filter_chats"
        )
    filter_messages = relationship(
        "FilterMessages",
        back_populates="filter_chat"
        )
    filter_professors = relationship(
        "FilterProfessors",
        back_populates="filter_chat"
        )

class FilterMessages(Base):
    __tablename__ = "filter_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
        )
    chat_id = Column(
        Integer,
        ForeignKey("filter_chats.id"),
        nullable=False,
        index=True
        )
    role = Column(
        String(20), 
        nullable=False
        )  # "user" or "assistant" or "system"
    content = Column(
        Text,
        nullable=False
        )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
        )
    filter_chat = relationship(
        "FilterChat",
        back_populates="filter_messages"
        )

class EmailChat(Base):
    __tablename__ = "email_chats"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    user_id = Column(
        Integer, 
        ForeignKey("users.id"), 
        nullable=False,
        index=True
        )
    title = Column(
        String(255), 
        nullable=False
        )
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
        )
    user = relationship(
        "User",
        back_populates="email_chats"
        )
    email_messages = relationship(
        "EmailMessages",
        back_populates="email_chat"
        )
    emails = relationship(
        "Email",
        back_populates="email_chat"
    )

class EmailMessages(Base):
    __tablename__ = "email_messages"

    id = Column(
        Integer,
        primary_key=True,
        index=True
        )
    chat_id = Column(
        Integer,
        ForeignKey("email_chats.id"),
        nullable=False,
        index=True
        )
    role = Column(
        String(20), 
        nullable=False
        )  # "user" or "assistant" or "system"
    content = Column(
        Text,
        nullable=False
        )
    created_at = Column(
        DateTime,
        default=datetime.utcnow
        )
    email_chat = relationship(
        "EmailChat",
        back_populates="email_messages"
        )

class Email(Base):
    __tablename__ = "emails"

    id = Column(
        Integer, 
        primary_key=True, 
        index=True
        )
    chat_id = Column(
        Integer,
        ForeignKey("email_chats.id"),
        nullable=False,
        index=True
        )
    email = Column(
        String, 
        unique=True, 
        nullable=False, 
        index=True
        )
    subject = Column(
        String, 
        nullable=True
        )
    body = Column(
        Text, 
        nullable=True
        )
    created_at = Column(
        DateTime, 
        default=datetime.utcnow
        )
    updated_at = Column(
        DateTime, 
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
        )
    email_chat = relationship(
        "EmailChat",
        back_populates="emails"
    )

class GmailAccounts(Base):
    __tablename__ = "gmail_accounts"

    id = Column(Integer, primary_key=True, index=True)

    # Your application's user
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    # Google's unique identifier (ID token "sub")
    google_user_id = Column(
        String,
        nullable=False,
        index=True
    )

    # Gmail address
    email = Column(
        String,
        nullable=False
    )

    # Google OAuth credentials
    access_token = Column(
        Text,
        nullable=False
    )

    refresh_token = Column(
        Text,
        nullable=False
    )

    access_token_expires_at = Column(
        DateTime,
        nullable=False
    )

    # Permissions granted by the user
    scopes = Column(
        Text,
        nullable=False
    )

    # Only one Gmail account should be active for a user
    is_active = Column(
        Boolean,
        default=True,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="gmail_accounts"
    )

class Professor(Base):
    __tablename__ = "professors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    name = Column(
        String,
        nullable=False,
        index=True
    )
    email = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    phone = Column(
        String,
        nullable=True
    )
    designation = Column(
        String,
        nullable=True
    )
    department = Column(
        String,
        nullable=True,
        index=True
    )
    institute = Column(
        String,
        nullable=True,
        index=True
    )
    research_area = Column(
        String,
        nullable=True
    )
    research_interests = Column(
        String,
        nullable=True
    )

class OAuthState(Base):

    __tablename__ = "oauth_states"

    id = Column(Integer, primary_key=True)

    state = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )

    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    expires_at = Column(
        DateTime,
        nullable=False
    )

    used = Column(
        Boolean,
        default=False,
        nullable=False
    )

    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )

    user = relationship(
        "User",
        back_populates="oauth_states"
    )

class FilterProfessors(Base):

    __tablename__ = "filter_professors"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    chat_id = Column(
        Integer,
        ForeignKey("filter_chats.id"),
        nullable=False,
        index=True
    )
    professor_id = Column(
        Integer,
        ForeignKey("professors.id"),
        nullable=False,
        index=True
    )
    filter_chat = relationship(
        "FilterChat",
        back_populates="filter_professors"
    )

class UserAPIKeys(Base):
    __tablename__ = "user_api_keys"

    id = Column(
        Integer,
        primary_key=True,
        index=True
    )
    user_id = Column(
        Integer,
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    api_key = Column(
        String,
        unique=True,
        nullable=False,
        index=True
    )
    created_at = Column(
        DateTime,
        default=datetime.utcnow,
        nullable=False
    )
    updated_at = Column(
        DateTime,
        default=datetime.utcnow,
        onupdate=datetime.utcnow,
        nullable=False
    )
    user = relationship(
        "User",
        back_populates="user_api_keys"
    )