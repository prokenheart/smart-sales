import pytest
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerIdPath
from pydantic import ValidationError
import uuid

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
            customer_name="Alice Peterson",
            customer_email="invalid-email",
            customer_phone="+12025550107"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert "email" in error["msg"].lower()

# Hợp lệ theo regex (không + nhưng bắt đầu [1-9], đủ dài)
def test_customer_create_valid_phone_no_plus():
    customer = CustomerCreate(
        customer_name="Alice Peterson",
        customer_email="alice.peterson@gmail.com",
        customer_phone="12025550107"  
    )
    assert customer.customer_name == "Alice Peterson"
    assert customer.customer_email == "alice.peterson@gmail.com"
    assert customer.customer_phone == "+12025550107"

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
def test_customer_create_invalid_phone(invalid_phone):
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson",
            customer_email="alice.peterson@gmail.com",
            customer_phone=invalid_phone
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()

# Thiếu customer_name
def test_customer_create_missing_name():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_email="alice.peterson@gmail.com",
            customer_phone="+12025550107"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_name",)
    assert error["type"] == "missing"

# Thiếu customer_email
def test_customer_create_missing_email():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson",
            customer_phone="+12025550107"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert error["type"] == "missing"

# Thiếu customer_phone
def test_customer_create_missing_phone():
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson",
            customer_email="alice.peterson@gmail.com"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert error["type"] == "missing"


# Truyền thiếu thông tin nhưng vẫn hợp lệ do optional
def test_customer_update_valid_partial():
    update = CustomerUpdate(
        customer_name="Alice Peterson",
        customer_phone="+12025550107"
    )
    assert update.customer_name == "Alice Peterson"
    assert update.customer_email is None
    assert update.customer_phone == "+12025550107"

# Email không hợp lệ (thiếu dấu @)
def test_customer_update_invalid_email():
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(
            customer_email="invalid-email"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
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
def test_customer_update_invalid_phone(invalid_phone):
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(
            customer_phone=invalid_phone
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

# Test kiểu dữ liệu id
def test_customer_id_path_valid():
    customer_id = uuid.uuid4()
    customer = CustomerIdPath(
        customer_id=customer_id
    )
    assert customer.customer_id == customer_id
    assert isinstance(customer.customer_id, uuid.UUID)

@pytest.mark.parametrize(
    "customer_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ]
)
def test_customer_id_path_invalid(customer_id):
    with pytest.raises(ValidationError) as exc_info:
        CustomerIdPath(
            customer_id=customer_id
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
    