from pydantic import ValidationError
import re
from enum import Enum
from app.database import get_db
from app.schemas.user import (
    UserCreate,
    UserIdPath,
    UserEmailQuery,
    UserResponse,
    UserUpdateInfo,
    UserUpdatePassword
)

from app.services.user import (
    create_user,
    get_user,
    get_all_users,
    get_user_by_account,
    get_user_by_email,
    update_user_info,
    update_user_password,
    verify_password,
    delete_user,
    search_users_by_account,
    search_users_by_email,
    search_users_by_phone,
    search_users_by_name,
    DuplicateAccountError,
    DuplicateEmailError
)

from app.core.response import success, error
class SearchType(str, Enum):
    EMAIL = "email"
    NAME = "name"
    PHONE = "phone"
    ACCOUNT = "account"

PHONE_REGEX = re.compile(r"^\+?\d{8,15}$")
UPPERCASE_REGEX = re.compile(r"[A-Z]")

def create_user_handler(body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        data = UserCreate.model_validate(body)
    except ValidationError as e:
        safe_errors = []
        for err in e.errors():
            safe_err = {k: v for k, v in err.items() if k != 'ctx'}  # loại bỏ 'ctx' chứa ValueError
            safe_errors.append(safe_err)
        
        return error(
            message="Invalid request body",
            status_code=400,
            details=safe_errors
        )
        
    try:
        with get_db() as db:
            user = create_user(
                db,
                data.user_name,
                data.user_email,
                data.user_phone,
                data.user_account,
                data.user_password
            )
            response = UserResponse.model_validate(user)
            return success(
                data=response,
                status_code=201
            )
    
    except DuplicateAccountError as e:
        return error(
            message=str(e),
            status_code=409
        )

    except DuplicateEmailError as e:
        return error(
            message=str(e),
            status_code=409
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_user_handler(user_id: str):
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError:
            return error(
                message="Invalid user_id",
                status_code=400
            )
    
    try:
        with get_db() as db:
            user = get_user(db, user_id)

            if not user:
                return error(
                    message="User not found",
                    status_code=404
                )
            
            response = UserResponse.model_validate(user)

            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )
    
def get_all_users_handler():
    try:
        with get_db() as db:
            users = get_all_users(db)
            return success([
                UserResponse.model_validate(user) for user in users
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_user_by_account_handler(user_account: str):
    try:
        with get_db() as db:
            user = get_user_by_account(db, user_account)

            if not user:
                return error(
                    message="User not found",
                    status_code=404
                )

            response = UserResponse.model_validate(user)
            return success(response)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def get_user_by_email_handler(user_email: str):
    try:
        user_email = UserEmailQuery.model_validate({"user_email": user_email}).user_email
    except ValidationError as e:
        return error(
            message="Invalid email parameter",
            status_code=400,
            details=e.errors()
        )

    try:
        with get_db() as db:
            user = get_user_by_email(db, user_email)

            if not user:
                return error(
                    message="User not found",
                    status_code=404
                )

            response = UserResponse.model_validate(user)
            return success(response)
    
    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def update_user_info_handler(user_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = UserUpdateInfo.model_validate(body)
    except ValidationError as e:
        safe_errors = []
        for err in e.errors():
            safe_err = {k: v for k, v in err.items() if k != 'ctx'}  # loại bỏ 'ctx' chứa ValueError
            safe_errors.append(safe_err)
        
        return error(
            message="Invalid request body",
            status_code=400,
            details=safe_errors
        )
    
    try:
        with get_db() as db:
            user = update_user_info(
                db,
                user_id,
                data.user_name,
                data.user_email,
                data.user_phone
            )

            if not user:
                return error(
                    message="User not found",
                    status_code=404
                )
            
            response = UserResponse.model_validate(user)
            return success(response)

    except DuplicateEmailError as e:
        return error(
            message=str(e),
            status_code=409
        )

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def update_user_password_handler(user_id: str, body: dict):
    if body is None:
        return error(
            message="Request body is required",
            status_code=400
        )
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    try:
        data = UserUpdatePassword.model_validate(body)
    except ValidationError as e:
        return error(
            message="Invalid request body",
            status_code=400,
            details=e.errors()
        )
    
    try:
        with get_db() as db:
            user = get_user(db, user_id)
            if not user:
                return error(
                    message="User not found",
                    status_code=404
                )

            if not verify_password(data.old_password, user.user_password):
                return error(
                    message="Old password is incorrect",
                    status_code=400
                )

            if verify_password(data.new_password, user.user_password):
                return error(
                    message="New password must be different from old password",
                    status_code=400
                )

            update_user_password(
                db,
                user_id,
                data.new_password
            )

            return success(status_code=204)

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def delete_user_handler(user_id: str):
    try:
        user_id = UserIdPath.model_validate({"user_id": user_id}).user_id
    except ValidationError as e:
        return error(
            message="Invalid user_id",
            status_code=400,
            details=e.errors()
        )
    
    try:
        with get_db() as db:
            deleted_id = delete_user(db, user_id)

            if not deleted_id:
                return error(
                    message="User not found",
                    status_code=404
                )

            return success(
                data={"user_id": str(deleted_id)}
            )   

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def search_users_handler(query: str):
    if not query or not query.strip():
        return error(
            message="Query parameter is required and cannot be empty",
            status_code=400
        )

    try:
        with get_db() as db:
            keyword = query.strip()
            search_type = detect_search_type(keyword)

            if search_type == SearchType.EMAIL:
                users = search_users_by_email(db, keyword)
            elif search_type == SearchType.PHONE:
                users = search_users_by_phone(db, keyword)
            elif search_type == SearchType.NAME:
                users = search_users_by_name(db, keyword)
            else:
                users = search_users_by_account(db, keyword)

            return success([
                UserResponse.model_validate(user) for user in users
            ])

    except Exception as e:
        return error(
            message="Internal server error",
            status_code=500,
            details=str(e)
        )

def detect_search_type(keyword: str) -> str:
    keyword = keyword.strip()
    if "@" in keyword:
        return SearchType.EMAIL
    if PHONE_REGEX.search(keyword):
        return SearchType.PHONE
    if UPPERCASE_REGEX.search(keyword) or " " in keyword:
        return SearchType.NAME
    return SearchType.ACCOUNT