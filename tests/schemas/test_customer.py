import pytest
from app.schemas.customer import CustomerCreate, CustomerUpdate
from pydantic import ValidationError

# Truyền đầy đủ thông tin
def test_customer_create_valid():
    customer = CustomerCreate(
        customer_name="Alice Peterson",
        customer_email="alice.peterson@gmail.com",
        customer_phone="+12025550107"
    )
    assert customer.customer_name == "Alice Peterson"
    assert customer.customer_email == "alice.peterson@gmail.com"
    assert customer.customer_phone == "+12025550107"

# Không phải email hợp lệ (thiếu dấu @)
def test_customer_create_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Bob Johnson",
            customer_email="invalid-email",
            customer_phone="+12025550108"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert "email" in error["msg"].lower()

# Hợp lệ theo regex (không + nhưng bắt đầu [1-9], đủ dài)
def test_customer_create_valid_phone_no_plus():
    customer = CustomerCreate(
        customer_name="Charlie Davis",
        customer_email="charlie.davis@example.com",
        customer_phone="12025550109"  
    )
    assert customer.customer_name == "Charlie Davis"
    assert customer.customer_email == "charlie.davis@example.com"
    assert customer.customer_phone == "12025550109"

# Số điện thoại quá ngắn
def test_customer_create_invalid_phone_too_short():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Dana Evans",
            customer_email="dana.evans@example.com",
            customer_phone="+123456"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Số điện thoại quá dài
def test_customer_create_invalid_phone_too_long():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Evan Foster",
            customer_email="evan.foster@example.com",
            customer_phone="+1234567890123456"  # 16 chữ số sau +, tổng >15
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Số điện thoại bắt đầu bằng 0
def test_customer_create_invalid_phone_starts_with_zero():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Fiona Green",
            customer_email="fiona.green@example.com",
            customer_phone="+0123456789"  # Bắt đầu bằng 0 sau +
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Số điện thoại có chữ cái
def test_customer_create_invalid_phone_non_digits():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="George Harris",
            customer_email="george.harris@example.com",
            customer_phone="+12345abcde"  # Chứa chữ cái
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Thiếu customer_name
def test_customer_create_missing_name():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_email="missing.name@example.com",
            customer_phone="+12025550110"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_name",)
    assert error["type"] == "missing"

# Thiếu customer_email
def test_customer_create_missing_email():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Missing Email",
            customer_phone="+12025550111"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert error["type"] == "missing"

# Thiếu customer_phone
def test_customer_create_missing_phone():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Missing Phone",
            customer_email="missing.phone@example.com"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert error["type"] == "missing"


# Truyền thiếu thông tin nhưng vẫn hợp lệ do optional
def test_customer_update_valid_partial():
    update = CustomerUpdate(
        customer_name="Updated Name",
        customer_phone="+12025550112"
    )
    assert update.customer_name == "Updated Name"
    assert update.customer_email is None
    assert update.customer_phone == "+12025550112"

# Email không hợp lệ (thiếu dấu @)
def test_customer_update_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(
            customer_email="invalid-email"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert "email" in error["msg"].lower()

# Số điện thoại bắt đầu bằng 0
def test_customer_update_invalid_phone():
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(
            customer_phone="+0123456789"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Pass do optional
def test_customer_update_none_phone():
    update = CustomerUpdate(
        customer_phone=None
    )
    assert update.customer_phone is None

def test_customer_update_all_none():
    update = CustomerUpdate()
    assert update.customer_name is None
    assert update.customer_email is None
    assert update.customer_phone is None