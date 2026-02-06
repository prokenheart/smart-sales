import pytest
from app.schemas.user import UserCreate, UserUpdateInfo, UserIdPath
from pydantic import ValidationError
import uuid


# Basic valid case
def test_user_create_valid() -> None:
    user = UserCreate(
        user_name="Alice Peterson",
        user_email="alice.peterson@gmail.com",
        user_phone="+12025550107",
        user_account="alice.peterson",
        user_password="12345678",
    )
    assert user.user_name == "Alice Peterson"
    assert user.user_email == "alice.peterson@gmail.com"
    assert user.user_phone == "+12025550107"
    assert user.user_account == "alice.peterson"
    assert user.user_password == "12345678"


# Invalid email format (missing @)
def test_user_create_invalid_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="invalid-email",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert "email" in error["msg"].lower()


# Valid phone without plus sign
def test_user_create_valid_phone_no_plus() -> None:
    user = UserCreate(
        user_name="Alice Peterson",
        user_email="alice.peterson@gmail.com",
        user_phone="12025550107",
        user_account="alice.peterson",
        user_password="12345678",
    )
    assert user.user_name == "Alice Peterson"
    assert user.user_email == "alice.peterson@gmail.com"
    assert user.user_phone == "+12025550107"
    assert user.user_account == "alice.peterson"
    assert user.user_password == "12345678"


# Invalid phone formats
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",  # Too short
        "+1234567890123456",  # Too long
        "+0123456789",  # Starts with 0
        "+12345abcde",  # Contains letters
    ],
)
def test_user_create_invalid_phone(invalid_phone: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone=invalid_phone,
            user_account="alice.peterson",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert "phone" in error["msg"].lower()


# Password too short
def test_user_create_password_too_short() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="12025550107",
            user_account="alice.peterson",
            user_password="1234567",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_password",)
    assert "at least 8 characters" in error["msg"].lower()


# Missing user_name
def test_user_create_missing_name() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_name",)
    assert error["type"] == "missing"


# Missing user_email
def test_user_create_missing_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert error["type"] == "missing"


# Missing user_phone
def test_user_create_missing_phone() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_account="alice.peterson",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert error["type"] == "missing"


# Missing user_account
def test_user_create_missing_account() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_password="12345678",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_account",)
    assert error["type"] == "missing"


# Missing user_password
def test_user_create_missing_password() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_account="alice.peterson",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_password",)
    assert error["type"] == "missing"


# Valid partial update (only name and phone)
def test_user_update_info_valid_partial() -> None:
    update = UserUpdateInfo(user_name="Alice Peterson", user_phone="+12025550107")
    assert update.user_name == "Alice Peterson"
    assert update.user_email is None
    assert update.user_phone == "+12025550107"


# Invalid email format
def test_user_update_info_invalid_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateInfo(user_email="invalid-email")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert "email" in error["msg"].lower()


# Invalid phone formats
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",  # Too short
        "+1234567890123456",  # Too long
        "+0123456789",  # Starts with 0
        "+12345abcde",  # Contains letters
    ],
)
def test_user_update_info_invalid_phone(invalid_phone: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateInfo(user_phone=invalid_phone)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert "phone" in error["msg"].lower()


# Test updating with None values
def test_user_update_info_none_phone() -> None:
    update = UserUpdateInfo(user_phone=None)
    assert update.user_phone is None


def test_user_update_info_all_none() -> None:
    update = UserUpdateInfo()
    assert update.user_name is None
    assert update.user_email is None
    assert update.user_phone is None


# Valid user_id path
def test_user_id_path_valid() -> None:
    user_id = uuid.uuid4()
    user = UserIdPath(user_id=user_id)
    assert user.user_id == user_id
    assert isinstance(user.user_id, uuid.UUID)


@pytest.mark.parametrize(
    "user_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ],
)
def test_user_id_path_invalid(user_id: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        UserIdPath(user_id=user_id)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
