from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from database import get_db
from auth import authenticate_user
from schemas.user import LoginRequest, LoginResponse, UserResponse

router = APIRouter(prefix="/api", tags=["auth"])
security = HTTPBasic()

# TODO v0.2: Implement rate limiting for login endpoints
# TODO v0.2: Enforce HTTPS-only connections in production


@router.post("/login", response_model=LoginResponse)
async def login(login_req: LoginRequest, db: Session = Depends(get_db)) -> LoginResponse:
    user = authenticate_user(db, login_req.username, login_req.password)
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect username or password",
        )
    return LoginResponse(success=True, message="Login successful", user=UserResponse.model_validate(user))


@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPBasicCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> UserResponse:
    user = authenticate_user(db, credentials.username, credentials.password)
    if not user:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return UserResponse.model_validate(user)
