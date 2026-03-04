from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from fastapi.security import OAuth2PasswordRequestForm
from pydantic import BaseModel, EmailStr, Field

from app.db.dependencies import get_db
from app.models.user import User
from app.schemas.user import UserCreate, UserResponse
from app.schemas.token import Token
from app.core.security import verify_password
from app.core.auth import create_access_token
from app.services import user_service
from app.core.config import ADMIN_SECRET


router = APIRouter(prefix="/users", tags=["Users"])


class AdminRegister(BaseModel):
    username: str = Field(min_length=3)
    email: EmailStr
    password: str = Field(min_length=8)
    admin_secret: str


@router.post("/register", response_model=UserResponse, status_code=201)
def register_user(user: UserCreate, db: Session = Depends(get_db)):
    return user_service.register_user(db, user)


@router.post("/register-admin", response_model=UserResponse, status_code=201)
def register_admin(user: AdminRegister, db: Session = Depends(get_db)):
    user_data = UserCreate(
        username=user.username,
        email=user.email,
        password=user.password,
    )
    return user_service.register_admin(db, user_data, user.admin_secret)


@router.post("/login", response_model=Token)
def login_user(
    form_data: OAuth2PasswordRequestForm = Depends(),
    db: Session = Depends(get_db),
):
    user = db.query(User).filter(User.email == form_data.username).first()

    if not user or not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials")

    access_token = create_access_token(data={"sub": str(user.id)})
    return {"access_token": access_token, "token_type": "bearer"}
