import pytest
from app.schemas.item import ItemCreate, ItemList
from pydantic import ValidationError
import uuid

# Truyền đầy đủ thông tin
def test_item_create_valid():
    product_id = uuid.uuid4()
    item = ItemCreate(
        product_id=product_id,
        item_quantity=5
    )
    assert item.product_id == product_id
    assert isinstance(item.product_id, uuid.UUID)
    assert item.item_quantity == 5

# Không phải id hợp lệ (định dạng đúng là uuid4)
def test_item_creat_invalid_product_id():
    invalid_product_id = "123-invalid-uuid"
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            product_id=invalid_product_id,
            item_quantity=5
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("product_id",)
    assert "UUID" in errors[0]["msg"]

# Số lượng nhỏ hơn hoặc bằng 0
@pytest.mark.parametrize("quantity", [0, -1, -10])
def test_item_create_invalid_quantity(quantity: int):
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            product_id=uuid.uuid4(),
            item_quantity=quantity
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "greater than 0" in errors[0]["msg"]

# Sai kiểu dữ liệu
def test_item_base_invalid_quantity_not_int():
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            product_id=uuid.uuid4(),
            item_quantity=3.5  # Không phải int
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "valid integer" in errors[0]["msg"]

# Thiếu product_id
def test_item_create_missing_product_id():
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            item_quantity=1
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_id",)
    assert error["type"] == "missing"

# Thiếu item_quantity
def test_item_create_missing_quantity():
    with pytest.raises(ValidationError) as exc_info:
        ItemCreate(
            product_id=uuid.uuid4()
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("item_quantity",)
    assert error["type"] == "missing"

# Tất cả các item trong list đều hợp lệ
def test_item_list_valid():
    items = [
        ItemCreate(product_id=uuid.uuid4(), item_quantity=2),
        ItemCreate(product_id=uuid.uuid4(), item_quantity=3)
    ]
    item_list = ItemList(list_item=items)
    assert len(item_list.list_item) == 2
    assert item_list.list_item[0].item_quantity == 2

# List rỗng
def test_item_list_empty():
    item_list = ItemList(list_item=[])
    assert len(item_list.list_item) == 0

# Một item trong list không hợp lệ
def test_item_list_with_invalid_item():
    with pytest.raises(ValidationError) as exc_info:
        ItemList(
            list_item=[
                ItemCreate(product_id=uuid.uuid4(), item_quantity=5),
                ItemCreate(product_id=uuid.uuid4(), item_quantity=0)    # Invalid
            ]
        )
    errors = exc_info.value.errors()

    assert errors[0]["loc"] == ("item_quantity",)
    assert "greater than 0" in errors[0]["msg"]