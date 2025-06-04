from fastapi import APIRouter, Depends, status
from fastapi.security import OAuth2PasswordRequestForm

from sqlalchemy.ext.asyncio import AsyncSession

from app.auth.schemas import Token, UserRegister
from app.dependencies.dao_dependency import get_session_with_commit
from app.auth.user_service import AuthService

from loguru import logger
router = APIRouter()


@router.post(
    "/register",
    response_model=dict,
    status_code=status.HTTP_201_CREATED,
    summary="Register a new user",
    description="Creates a new user with a unique username and hashed password.",
    responses={
        201: {"description": "User created successfully"},
        409: {"description": "User already exists"},
    },
)
async def register(
    user_data: UserRegister,
    session: AsyncSession = Depends(get_session_with_commit),
) -> dict[str, str]:
    user = await AuthService.register(session, user_data)
    logger.info(f"User registered: {user.get('username', 'unknown')}")
    return user

@router.post(
    "/login",
    response_model=Token,
    summary="Login user and get JWT token",
    description="Authenticate user and return JWT access token.",
    responses={
        200: {"description": "Login successful, JWT returned"},
        400: {"description": "Incorrect username or password"},
    },
)
async def login(
    session: AsyncSession = Depends(get_session_with_commit),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> dict[str, str]:
    user = await AuthService.authenticate(session, form_data.username, form_data.password)
    access_token = AuthService.create_token(user.id)
    logger.info(f"User logged in: {user.username}")
    return {"access_token": access_token, "token_type": "bearer"}




