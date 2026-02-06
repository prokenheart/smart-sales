import pytest
from app.schemas.product import ProductCreate, ProductUpdate, ProductIdPath
from pydantic import ValidationError
import uuid


# Basic valid case
def test_product_create_valid() -> None:
    product = ProductCreate(
        product_name="Acer Swift 3 Laptop",
        product_description="A modern laptop",
        product_quantity=50,
    )
    assert product.product_name == "Acer Swift 3 Laptop"
    assert product.product_description == "A modern laptop"
    assert product.product_quantity == 50


# Valid case without product_description
def test_product_create_valid_description() -> None:
    product = ProductCreate(product_name="Acer Swift 3 Laptop", product_quantity=50)

    assert product.product_name == "Acer Swift 3 Laptop"
    assert product.product_description is None
    assert product.product_quantity == 50


# product_quantity < 0
@pytest.mark.parametrize("product_quantity", [-1, -10, -100])
def test_product_create_invalid_quantity(product_quantity: int) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            product_name="Acer Swift 3 Laptop",
            product_description="A modern laptop",
            product_quantity=product_quantity,
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_quantity",)
    assert "greater than or equal to 0" in error["msg"].lower()


# product_quantity not int
@pytest.mark.parametrize("product_quantity", [1.5, 9.1])
def test_product_create_invalid_quantity_not_int(product_quantity: float) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            product_name="Acer Swift 3 Laptop",
            product_description="A modern laptop",
            product_quantity=product_quantity,
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_quantity",)
    assert "valid integer" in error["msg"].lower()


# Missing product_name
def test_product_create_missing_name() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(product_description="A modern laptop", product_quantity=50)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_name",)
    assert error["type"] == "missing"


# Missing product_quantity
def test_product_create_missing_quantity() -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductCreate(
            product_name="Acer Swift 3 Laptop", product_description="A modern laptop"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_quantity",)
    assert error["type"] == "missing"


# Test ProductUpdate schema
def test_product_update_valid_partial() -> None:
    update = ProductUpdate(product_description="A modern laptop", product_quantity=50)
    assert update.product_name is None
    assert update.product_description == "A modern laptop"
    assert update.product_quantity == 50


# product_quantity < 0
@pytest.mark.parametrize("product_quantity", [-1, -10, -100])
def test_product_update_invalid_quantity(product_quantity: int) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductUpdate(product_quantity=product_quantity)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_quantity",)
    assert "greater than or equal to 0" in error["msg"].lower()


# product_quantity not int
@pytest.mark.parametrize("product_quantity", [1.5, 9.1])
def test_product_update_invalid_quantity_not_int(product_quantity: float) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductUpdate(product_quantity=product_quantity)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_quantity",)
    assert "valid integer" in error["msg"].lower()


# Missing all fields (all optional)
def test_product_update_none_quantity() -> None:
    update = ProductUpdate(product_quantity=None)
    assert update.product_quantity is None


def test_product_update_all_none() -> None:
    update = ProductUpdate()
    assert update.product_name is None
    assert update.product_description is None
    assert update.product_quantity is None


# Valid product_id path
def test_product_id_path_valid() -> None:
    product_id = uuid.uuid4()
    product = ProductIdPath(product_id=product_id)
    assert product.product_id == product_id
    assert isinstance(product.product_id, uuid.UUID)


@pytest.mark.parametrize(
    "product_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ],
)
def test_product_id_path_invalid(product_id: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        ProductIdPath(product_id=product_id)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("product_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
