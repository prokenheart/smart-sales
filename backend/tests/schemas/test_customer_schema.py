import pytest
from app.schemas.customer import CustomerCreate, CustomerUpdate, CustomerIdPath
from pydantic import ValidationError
import uuid


# Basic valid case
def test_customer_create_valid() -> None:
    customer = CustomerCreate(
        customer_name="Alice Peterson",
        customer_email="alice.peterson@gmail.com",
        customer_phone="+12025550107",
    )
    assert customer.customer_name == "Alice Peterson"
    assert customer.customer_email == "alice.peterson@gmail.com"
    assert customer.customer_phone == "+12025550107"


# Invalid email format (missing @)
def test_customer_create_invalid_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson",
            customer_email="invalid-email",
            customer_phone="+12025550107",
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert "email" in error["msg"].lower()


# Valid phone without plus sign
def test_customer_create_valid_phone_no_plus() -> None:
    customer = CustomerCreate(
        customer_name="Alice Peterson",
        customer_email="alice.peterson@gmail.com",
        customer_phone="12025550107",
    )
    assert customer.customer_name == "Alice Peterson"
    assert customer.customer_email == "alice.peterson@gmail.com"
    assert customer.customer_phone == "+12025550107"


# Phone number tests
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",  # Too short
        "+1234567890123456",  # Too long
        "+0123456789",  # Starts with 0
        "+12345abcde",  # Contains letters
    ],
)
def test_customer_create_invalid_phone(invalid_phone: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson",
            customer_email="alice.peterson@gmail.com",
            customer_phone=invalid_phone,
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()


# Missing customer_name
def test_customer_create_missing_name() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_email="alice.peterson@gmail.com", customer_phone="+12025550107"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_name",)
    assert error["type"] == "missing"


# Missing customer_email
def test_customer_create_missing_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(customer_name="Alice Peterson", customer_phone="+12025550107")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert error["type"] == "missing"


# Missing customer_phone
def test_customer_create_missing_phone() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerCreate(
            customer_name="Alice Peterson", customer_email="alice.peterson@gmail.com"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert error["type"] == "missing"


# Partial valid update
def test_customer_update_valid_partial() -> None:
    update = CustomerUpdate(
        customer_name="Alice Peterson", customer_phone="+12025550107"
    )
    assert update.customer_name == "Alice Peterson"
    assert update.customer_email is None
    assert update.customer_phone == "+12025550107"


# Invalid email format on update
def test_customer_update_invalid_email() -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(customer_email="invalid-email")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_email",)
    assert "email" in error["msg"].lower()


def test_customer_update_valid_phone_no_plus() -> None:
    update = CustomerUpdate(customer_phone="12025550107")
    assert update.customer_phone == "+12025550107"


# Phone number tests on update
@pytest.mark.parametrize(
    "invalid_phone",
    [
        "+123456",  # Too short
        "+1234567890123456",  # Too long
        "+0123456789",  # Starts with 0
        "+12345abcde",  # Contains letters
    ],
)
def test_customer_update_invalid_phone(invalid_phone: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerUpdate(customer_phone=invalid_phone)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_phone",)
    assert "phone" in error["msg"].lower()


# Update with None phone
def test_customer_update_none_phone() -> None:
    update = CustomerUpdate(customer_phone=None)
    assert update.customer_phone is None


# Update with all fields None
def test_customer_update_all_none() -> None:
    update = CustomerUpdate()
    assert update.customer_name is None
    assert update.customer_email is None
    assert update.customer_phone is None


# Test customer_id path
def test_customer_id_path_valid() -> None:
    customer_id = uuid.uuid4()
    customer = CustomerIdPath(customer_id=customer_id)
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
    ],
)
def test_customer_id_path_invalid(customer_id: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        CustomerIdPath(customer_id=customer_id)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
