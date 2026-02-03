import pytest
from app.schemas.order import OrderCreate, OrderIdPath
from pydantic import ValidationError
import uuid

# Truyền đầy đủ thông tin
def test_order_create_valid():
    customer_id = uuid.uuid4()
    user_id = uuid.uuid4()
    order = OrderCreate(
        customer_id=customer_id,
        user_id=user_id
    )
    assert order.customer_id == customer_id
    assert order.user_id == user_id

# Không phải customer_id hợp lệ
def test_order_create_invalid_customer_id():
    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(
            customer_id='123',
            user_id=uuid.uuid4()
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_id",)
    assert "uuid" in error["msg"].lower()

# Không phải user_id hợp lệ
def test_order_create_invalid_user_id():
    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(
            customer_id=uuid.uuid4(),
            user_id='123'
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_id",)
    assert "uuid" in error["msg"].lower()

# Thiếu customer_id
def test_order_create_missing_customer_id():
    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(
            user_id=uuid.uuid4()
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("customer_id",)
    assert error["type"] == "missing"

# Thiếu user_id
def test_order_create_missing_user_id():
    with pytest.raises(ValidationError) as exc_info:
        OrderCreate(
            customer_id=uuid.uuid4()
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("user_id",)
    assert error["type"] == "missing"

# Test kiểu dữ liệu id
def test_order_id_path_valid():
    order_id = uuid.uuid4()
    order = OrderIdPath(
        order_id=order_id
    )
    assert order.order_id == order_id
    assert isinstance(order.order_id, uuid.UUID)

@pytest.mark.parametrize(
    "order_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ]
)
def test_order_id_path_invalid(order_id: str):
    with pytest.raises(ValidationError) as exc_info:
        OrderIdPath(
            order_id=order_id
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("order_id",)
    assert "input should be a valid uuid" in error["msg"].lower()