import pytest
from app.schemas.user import UserCreate, UserUpdateInfo, UserIdPath
from pydantic import ValidationError
import uuid

# Truyền đầy đủ thông tin
def test_user_create_valid():
    user = UserCreate(
        user_name="Alice Peterson",
        user_email="alice.peterson@gmail.com",
        user_phone="+12025550107",
        user_account="alice.peterson",
        user_password="12345678"
    )
    assert user.user_name == "Alice Peterson"
    assert user.user_email == "alice.peterson@gmail.com"
    assert user.user_phone == "+12025550107"
    assert user.user_account == "alice.peterson"
    assert user.user_password == "12345678"

# Không phải email hợp lệ (thiếu dấu @)
def test_user_create_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="invalid-email",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert "email" in error["msg"].lower()

# Hợp lệ theo regex (không + nhưng bắt đầu [1-9], đủ dài)
def test_user_create_valid_phone_no_plus():
    user = UserCreate(
        user_name="Alice Peterson",
        user_email="alice.peterson@gmail.com",
        user_phone="12025550107",
        user_account="alice.peterson",
        user_password="12345678"
    )
    assert user.user_name == "Alice Peterson"
    assert user.user_email == "alice.peterson@gmail.com"
    assert user.user_phone == "+12025550107"
    assert user.user_account == "alice.peterson"
    assert user.user_password == "12345678"

# Số điện thoại
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",              # Quá ngắn
        "+1234567890123456",    # Quá dài
        "+0123456789",          # Bắt đầu bằng 0
        "+12345abcde"           # Chứa chữ cái
    ]
)
def test_user_create_invalid_phone(invalid_phone):
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone=invalid_phone,
            user_account="alice.peterson",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert "phone" in error["msg"].lower()

# Password quá ngắn
def test_user_create_password_too_short():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="12025550107",
            user_account="alice.peterson",
            user_password="1234567"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_password",)
    assert "at least 8 characters" in error["msg"].lower()

# Thiếu user_name
def test_user_create_missing_name():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_name",)
    assert error["type"] == "missing"

# Thiếu user_email
def test_user_create_missing_email():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_phone="+12025550107",
            user_account="alice.peterson",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert error["type"] == "missing"

# Thiếu user_phone
def test_user_create_missing_phone():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_account="alice.peterson",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert error["type"] == "missing"

# Thiếu user_account
def test_user_create_missing_account():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_password="12345678"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_account",)
    assert error["type"] == "missing"

# Thiếu user_password
def test_user_create_missing_password():
    with pytest.raises(ValidationError) as exc_info:
        UserCreate(
            user_name="Alice Peterson",
            user_email="alice.peterson@gmail.com",
            user_phone="+12025550107",
            user_account="alice.peterson"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_password",)
    assert error["type"] == "missing"


# Truyền thiếu thông tin nhưng vẫn hợp lệ do optional
def test_user_update_info_valid_partial():
    update = UserUpdateInfo(
        user_name="Alice Peterson",
        user_phone="+12025550107"
    )
    assert update.user_name == "Alice Peterson"
    assert update.user_email is None
    assert update.user_phone == "+12025550107"

# Email không hợp lệ (thiếu dấu @)
def test_user_update_info_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateInfo(
            user_email="invalid-email"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_email",)
    assert "email" in error["msg"].lower()

# Số điện thoại
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",              # Quá ngắn
        "+1234567890123456",    # Quá dài
        "+0123456789",          # Bắt đầu bằng 0
        "+12345abcde"           # Chứa chữ cái
    ]
)
def test_user_update_info_invalid_phone(invalid_phone):
    with pytest.raises(ValidationError) as exc_info:
        UserUpdateInfo(
            user_phone=invalid_phone
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_phone",)
    assert "phone" in error["msg"].lower()

# Pass do optional
def test_user_update_info_none_phone():
    update = UserUpdateInfo(
        user_phone=None
    )
    assert update.user_phone is None

def test_user_update_info_all_none():
    update = UserUpdateInfo()
    assert update.user_name is None
    assert update.user_email is None
    assert update.user_phone is None

# Test kiểu dữ liệu id
def test_user_id_path_valid():
    user_id = uuid.uuid4()
    user = UserIdPath(
        user_id=user_id
    )
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
    ]
)
def test_user_id_path_invalid(user_id):
    with pytest.raises(ValidationError) as exc_info:
        UserIdPath(
            user_id=user_id
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_id",)
    assert "input should be a valid uuid" in error["msg"].lower()