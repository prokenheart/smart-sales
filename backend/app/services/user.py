from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import select
from app.models import User
import uuid
from passlib.context import CryptContext


class DuplicateEmailError(Exception):
    pass


class DuplicateAccountError(Exception):
    pass


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def hash_password(password: str) -> str:
    return pwd_context.hash(password)


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def create_user(
    db: Session,
    user_name: str,
    user_email: str,
    user_phone: str,
    user_account: str,
    user_password: str,
) -> User:
    if get_user_by_account(db, user_account):
        raise DuplicateAccountError("Account already exists")

    if get_user_by_email(db, user_email):
        raise DuplicateEmailError("Email already exists")

    user = User(
        user_name=user_name,
        user_email=user_email,
        user_phone=user_phone,
        user_account=user_account,
        user_password=hash_password(user_password),
    )

    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        error_msg = str(e.orig)

        if "users_user_account_key" in error_msg:
            raise DuplicateAccountError("Account already exists")

        if "users_user_email_key" in error_msg:
            raise DuplicateEmailError("Email already exists")

        raise
    db.refresh(user)
    return user


def get_user(db: Session, user_id: uuid.UUID) -> User | None:
    stmt = select(User).where(User.user_id == user_id)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_account(db: Session, user_account: str) -> User | None:
    stmt = select(User).where(User.user_account == user_account)
    return db.execute(stmt).scalar_one_or_none()


def get_user_by_email(db: Session, user_email: str) -> User | None:
    stmt = select(User).where(User.user_email == user_email)
    return db.execute(stmt).scalar_one_or_none()


def get_all_users(db: Session) -> list[User]:
    stmt = select(User)
    return db.execute(stmt).scalars().all()


def update_user_info(
    db: Session,
    user_id: uuid.UUID,
    user_name: str | None = None,
    user_email: str | None = None,
    user_phone: str | None = None,
) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None

    if user_email and user_email != user.user_email:
        if get_user_by_email(db, user_email):
            raise DuplicateEmailError("Email already exists")
        user.user_email = user_email

    if user_name:
        user.user_name = user_name
    if user_phone:
        user.user_phone = user_phone

    db.add(user)
    try:
        db.commit()
    except IntegrityError as e:
        db.rollback()

        error_msg = str(e.orig)

        if "users_user_account_key" in error_msg:
            raise DuplicateAccountError("Account already exists")

        if "users_user_email_key" in error_msg:
            raise DuplicateEmailError("Email already exists")

        raise
    db.refresh(user)
    return user


def update_user_password(db: Session, user_id: uuid.UUID, new_password: str):
    user = get_user(db, user_id)

    user.user_password = hash_password(new_password)

    db.add(user)
    db.commit()
    db.refresh(user)


def delete_user(db: Session, user_id: uuid.UUID) -> uuid.UUID | None:
    user = get_user(db, user_id)
    if not user:
        return None

    db.delete(user)
    db.commit()
    return user_id


def search_users_by_account(db: Session, account_query: str) -> list[User]:
    stmt = select(User).where(User.user_account.ilike(f"%{account_query}%"))
    return db.execute(stmt).scalars().all()


def search_users_by_name(db: Session, name_query: str) -> list[User]:
    stmt = select(User).where(User.user_name.ilike(f"%{name_query}%"))
    return db.execute(stmt).scalars().all()


def search_users_by_email(db: Session, email_query: str) -> list[User]:
    stmt = select(User).where(User.user_email.ilike(f"%{email_query}%"))
    return db.execute(stmt).scalars().all()


def search_users_by_phone(db: Session, phone_query: str) -> list[User]:
    stmt = select(User).where(User.user_phone.ilike(f"%{phone_query}%"))
    return db.execute(stmt).scalars().all()
