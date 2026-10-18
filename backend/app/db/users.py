from sqlalchemy import select

from app.db.session import SessionLocal
from app.models.user import User


def get_user_by_email(email: str) -> User | None:
    with SessionLocal() as db:
        return db.scalar(select(User).where(User.email == email))


def get_user_by_id(user_id: int) -> User | None:
    with SessionLocal() as db:
        return db.get(User, user_id)


def create_user(email: str, hashed_password: str) -> User:
    with SessionLocal() as db:
        user = User(email=email, hashed_password=hashed_password)
        db.add(user)
        db.commit()
        db.refresh(user)
        return user