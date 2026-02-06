import pytest
from app.schemas.item import ItemCreate, ItemList
from pydantic import ValidationError
import uuid


# Basic valid case
def test_item_create_valid() -> None:
    product_id = uuid.uuid4()
    item = ItemCreate(product_id=product_id, item_quantity=5)
    assert item.product_id == product_id
    assert isinstance(item.product_id, uuid.UUID)
    assert item.item_quantity == 5


# Non-valid product_id (not a uuid4 format)
def test_item_create_invalid_product_id() -> None:
    invalid_product_id = "123-invalid-uuid"
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(product_id=invalid_product_id, item_quantity=5)
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("product_id",)
    assert "UUID" in errors[0]["msg"]


# Quantity less than or equal to 0
@pytest.mark.parametrize("quantity", [0, -1, -10])
def test_item_create_invalid_quantity(quantity: int) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(product_id=uuid.uuid4(), item_quantity=quantity)
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "greater than 0" in errors[0]["msg"]


# Quantity not int
def test_item_base_invalid_quantity_not_int() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            product_id=uuid.uuid4(),
            item_quantity=3.5,
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "valid integer" in errors[0]["msg"]


# Missing product_id
def test_item_create_missing_product_id() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(item_quantity=1)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_id",)
    assert error["type"] == "missing"


# Missing item_quantity
def test_item_create_missing_quantity() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(product_id=uuid.uuid4())
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("item_quantity",)
    assert error["type"] == "missing"


# Valid list of items
def test_item_list_valid() -> None:
    items = [
        ItemCreate(product_id=uuid.uuid4(), item_quantity=2),
        ItemCreate(product_id=uuid.uuid4(), item_quantity=3),
    ]
    item_list = ItemList(list_item=items)
    assert len(item_list.list_item) == 2
    assert item_list.list_item[0].item_quantity == 2


# Empty list of items
def test_item_list_empty() -> None:
    item_list = ItemList(list_item=[])
    assert len(item_list.list_item) == 0


# List with one invalid item (quantity <= 0)
def test_item_list_with_invalid_item() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ItemList(
            list_item=[
                ItemCreate(product_id=uuid.uuid4(), item_quantity=5),
                ItemCreate(product_id=uuid.uuid4(), item_quantity=0),  # Invalid
            ]
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "greater than 0" in errors[0]["msg"]
