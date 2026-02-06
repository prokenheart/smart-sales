import pytest
from app.schemas.price import PriceCreate, PriceUpdate, PriceIdPath
from pydantic import ValidationError
import uuid
from decimal import Decimal
from datetime import date


# Basic valid case
def test_price_create_valid():
    product_id = uuid.uuid4()
    price = PriceCreate(
        product_id=product_id, price_amount=100, price_date="2026-01-27"
    )
    assert price.product_id == product_id
    assert isinstance(price.product_id, uuid.UUID)
    assert price.price_amount == Decimal("100")
    assert price.price_date == date(2026, 1, 27)


# Non-valid product_id (not a uuid4 format)
def test_price_create_invalid_product_id():
    invalid_product_id = "123-invalid-uuid"
    with pytest.raises(ValidationError) as exc_info:
        PriceCreate(
            product_id=invalid_product_id, price_amount=100, price_date="2026-01-27"
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("product_id",)
    assert "UUID" in errors[0]["msg"]


# price_amount <= 0
@pytest.mark.parametrize("amount", [0, -1.5, -10])
def test_price_create_invalid_amount(amount: float):
    with pytest.raises(ValidationError) as exc_info:
        PriceCreate(
            product_id=uuid.uuid4(), price_amount=amount, price_date="2026-01-27"
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("price_amount",)
    assert "greater than 0" in errors[0]["msg"]


# Missing product_id
def test_price_create_missing_product_id():
    with pytest.raises(ValidationError) as exc_info:
        PriceCreate(price_amount=1, price_date="2026-01-27")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_id",)
    assert error["type"] == "missing"


# Missing price_amount
def test_price_create_missing_amount():
    with pytest.raises(ValidationError) as exc_info:
        PriceCreate(product_id=uuid.uuid4(), price_date="2026-01-27")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("price_amount",)
    assert error["type"] == "missing"


# Missing price_date
def test_price_create_missing_date():
    with pytest.raises(ValidationError) as exc_info:
        PriceCreate(product_id=uuid.uuid4(), price_amount=1)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("price_date",)
    assert error["type"] == "missing"


# Test PriceUpdate schema
def test_price_update_valid_partial():
    update = PriceUpdate(price_amount=100, price_date="2026-01-27")
    assert update.product_id is None
    assert update.price_amount == Decimal("100")
    assert update.price_date == date(2026, 1, 27)


# price_amount <= 0
@pytest.mark.parametrize("price_amount", [-1.5, -10, 0])
def test_price_update_invalid_quantity(price_amount: float) -> None:
    with pytest.raises(ValidationError) as exc_info:
        PriceUpdate(price_amount=price_amount)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("price_amount",)
    assert "greater than 0" in error["msg"].lower()


# Test PriceUpdate with None values
def test_price_update_none_quantity() -> None:
    update = PriceUpdate(price_amount=None)
    assert update.price_amount is None


def test_price_update_all_none() -> None:
    update = PriceUpdate()
    assert update.product_id is None
    assert update.price_amount is None
    assert update.price_date is None


# Test price_id path
def test_price_id_path_valid() -> None:
    price_id = uuid.uuid4()
    price = PriceIdPath(price_id=price_id)
    assert price.price_id == price_id
    assert isinstance(price.price_id, uuid.UUID)


@pytest.mark.parametrize(
    "price_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ],
)
def test_price_id_path_invalid(price_id: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        PriceIdPath(price_id=price_id)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("price_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
