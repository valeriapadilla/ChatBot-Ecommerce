from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse
from app.services.auth.auth_service import AuthService
from app.services.auth.jwt_service import JWTService
from app.models.user import User
from db.session import SessionLocal

router = APIRouter(prefix="/auth", tags=["authentication"])

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/register", response_model=TokenResponse)
async def register(user_data: UserRegister, db: Session = Depends(get_db)):
    existing_user = AuthService.get_user_by_email(db, user_data.email)
    if existing_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user = AuthService.create_user(
        db=db,
        email=user_data.email,
        password=user_data.password,
        name=user_data.name
    )
    
    access_token = JWTService.create_user_token(user)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            name=user.name
        )
    )

@router.post("/login", response_model=TokenResponse)
async def login(user_data: UserLogin, db: Session = Depends(get_db)):
    user = AuthService.authenticate_user(db, user_data.email, user_data.password)
    if not user:
        raise HTTPException(status_code=401, detail="Invalid credentials")
    
    access_token = JWTService.create_user_token(user)
    
    return TokenResponse(
        access_token=access_token,
        user=UserResponse(
            name=user.name
        )
    ) 