from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.auth import UserRegister, UserLogin, TokenResponse, UserResponse, LogoutResponse
from app.services.auth.auth_service import AuthService
from app.services.auth.jwt_service import JWTService
from app.models.user import User
from app.api.deps import get_db, get_current_user
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from db.session import SessionLocal

router = APIRouter(prefix="/auth", tags=["authentication"])
security = HTTPBearer()

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

@router.post("/signup", response_model=TokenResponse)
async def signup(user_data: UserRegister, db: Session = Depends(get_db)):
    """Alias for register endpoint to match frontend expectations"""
    return await register(user_data, db)

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

@router.post("/logout", response_model=LogoutResponse)
async def logout(
    current_user: User = Depends(get_current_user),
    credentials: HTTPAuthorizationCredentials = Depends(security)
):
    """Logout endpoint - blacklists the token and requires valid authentication"""
    JWTService.blacklist_token(credentials.credentials)
    JWTService.cleanup_expired_tokens()
    
    return LogoutResponse()

@router.get("/me", response_model=UserResponse)
async def get_current_user_info(current_user: User = Depends(get_current_user)):
    """Get current user information"""
    return UserResponse(
        name=current_user.name
    ) 