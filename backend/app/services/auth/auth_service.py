import logging
from passlib.context import CryptContext
from sqlalchemy.orm import Session
from app.models.user import User
from app.interfaces.auth_interface import AuthServiceInterface

logger = logging.getLogger(__name__)

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

class AuthService(AuthServiceInterface):
    """Service for authentication and user management."""
    
    @staticmethod
    def hash_password(password: str) -> str:
        """Hash a password using bcrypt."""
        return pwd_context.hash(password)
    
    @staticmethod
    def verify_password(plain_password: str, hashed_password: str) -> bool:
        """Verify a password against its hash."""
        return pwd_context.verify(plain_password, hashed_password)
    
    @staticmethod
    def create_user(db: Session, email: str, password: str, name: str = None) -> User:
        """Create a new user with hashed password."""
        try:
            hashed_password = AuthService.hash_password(password)
            
            user = User(
                email=email,
                password=hashed_password,
                name=name,
                is_active=True
            )
            
            db.add(user)
            db.commit()
            db.refresh(user)
            
            logger.info("User created successfully: %s", email)
            return user
            
        except Exception as e:
            db.rollback()
            logger.error("Failed to create user %s: %s", email, str(e))
            raise
    
    @staticmethod
    def authenticate_user(db: Session, email: str, password: str) -> User:
        """Authenticate a user by email and password."""
        try:
            user = db.query(User).filter(User.email == email).first()
            
            if not user:
                logger.warning("Authentication failed: user not found - %s", email)
                return None
            
            if not AuthService.verify_password(password, user.password):
                logger.warning("Authentication failed: invalid password - %s", email)
                return None
            
            if not user.is_active:
                logger.warning("Authentication failed: inactive user - %s", email)
                return None
            
            logger.info("User authenticated successfully: %s", email)
            return user
            
        except Exception as e:
            logger.error("Authentication error for %s: %s", email, str(e))
            raise
    
    @staticmethod
    def get_user_by_email(db: Session, email: str) -> User:
        """Get user by email."""
        return db.query(User).filter(User.email == email).first()
    
    @staticmethod
    def get_user_by_id(db: Session, user_id: int) -> User:
        """Get user by ID."""
        return db.query(User).filter(User.id == user_id).first() 