import jwt
from jwt.exceptions import InvalidTokenError
from fastapi import Depends,HTTPException
from fastapi.security import HTTPBearer,HTTPAuthorizationCredentials
from app.core.security import decode_access_token
from app.db.users import get_user_by_id

bearer_scheme=HTTPBearer(auto_error=False)

def get_current_user(
    credentials:HTTPAuthorizationCredentials | None = Depends(
        bearer_scheme
    ),
):
    if credentials is None:
        raise HTTPException(
            status_code=401,
            detail="Authentication required",
            headers={"WWW-Authenticate":"Bearer"}
        )

    try:
        payload=decode_access_token(credentials.credentials)
        user_id=payload.get("sub")
        if not isinstance(user_id, str) or not user_id.isdecimal():
            raise HTTPException(
                status_code=401,
                detail="Invalid token",
                headers={"WWW-Authenticate":"Bearer"}
            )
    except InvalidTokenError:
        raise HTTPException(
            status_code=401,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate":"Bearer"}
        ) from None
    user=get_user_by_id(int(user_id))
    if user is None:
        raise HTTPException(
            status_code=401,
            detail="User no longer exists"
        )
    return user