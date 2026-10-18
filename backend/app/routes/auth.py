from fastapi import APIRouter, Depends, HTTPException, status
from app.schemas.auth import(
    RegisterRequest,
    LoginRequest,
    UserResponse,
    TokenResponse
)
from app.core.security import(
    hash_password,
    verify_password,
    create_access_token
)

from app.db.users import(
    get_user_by_email,
    create_user
)

from app.dependencies.auth import get_current_user

router=APIRouter(prefix="/auth",tags=["Authentication"])
       

@router.post("/register",
    response_model=UserResponse,
    status_code=status.HTTP_201_CREATED)
def register(data:RegisterRequest):
    existing_user = get_user_by_email(data.email)
    if existing_user:
        raise HTTPException(
            status_code=409,
            detail="An account with email already exists"

        )   
    user=create_user(
        email=data.email,
        hashed_password=hash_password(data.password)
    )
    return UserResponse(id=str(user.id),email=user.email)

@router.post("/login",response_model=TokenResponse)
def login(data:LoginRequest):
    user = get_user_by_email(data.email)
    if( not user 
        or not verify_password(
            data.password,
            user.hashed_password
        )):
        raise HTTPException(
            status_code=401,
            detail="Invalid email or password",
            headers={"WWW-Authenticate": "Bearer"}
        )
    token=create_access_token(str(user.id))
    return TokenResponse(access_token=token)


@router.get("/me",response_model=UserResponse)
def get_me(user=Depends(get_current_user)):
    return UserResponse(id=str(user.id),email=user.email)
