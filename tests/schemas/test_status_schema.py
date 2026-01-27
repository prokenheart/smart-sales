import pytest
from app.schemas.status import StatusBase, StatusIdPath, StatusCode
from pydantic import ValidationError
import uuid

# Truyền đầy đủ thông tin
def test_status_base_valid():
    status = StatusBase(
        status_name="Unpaid",
        status_code="UNPAID"
    )
    assert status.status_name == "Unpaid"
    assert status.status_code == "UNPAID"

# Tự upper
def test_status_base_upper():
    status = StatusBase(
        status_name="Unpaid",
        status_code="Unpaid"
    )
    assert status.status_name == "Unpaid"
    assert status.status_code == "UNPAID"

@pytest.mark.parametrize(
    "status_code",
    [
        "",
        "unpaid2",
        "unpaid@"
    ]
)
# Sai kiểu status_code
def test_status_base_invalid_code(status_code):
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(
            status_name="Unpaid",
            status_code=status_code
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert "only uppercase letters" in error["msg"].lower()


# Thiếu status_name
def test_status_base_missing_status_name():
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(
            status_code="UNPAID"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_name",)
    assert error["type"] == "missing"

# Thiếu status_code
def test_status_base_missing_status_code():
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(
            status_name="Unpaid"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert error["type"] == "missing"

# Test kiểu dữ liệu status_code
def test_status_code_valid():
    status = StatusCode(
        status_code="PAID"
    )
    assert status.status_code == "PAID"

@pytest.mark.parametrize(
    "status_code",
    [
        "",
        "paid2",
        "paid@"
    ]
)
def test_status_code_invalid(status_code):
    with pytest.raises(ValidationError) as exc_info:
        StatusCode(
            status_code=status_code
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert "only uppercase letters" in error["msg"].lower()

# Test kiểu dữ liệu id
def test_status_id_path_valid():
    status_id = uuid.uuid4()
    status = StatusIdPath(
        status_id=status_id
    )
    assert status.status_id == status_id
    assert isinstance(status.status_id, uuid.UUID)

@pytest.mark.parametrize(
    "status_id",
    [
        "",
        "abc123",
        "12345678-1234-1234-1234",
        "zzzzzzzz-zzzz-zzzz-zzzz-zzzzzzzzzzzz",
        str(uuid.uuid4())[:-1] + "@",
    ]
)
def test_status_id_path_invalid(status_id):
    with pytest.raises(ValidationError) as exc_info:
        StatusIdPath(
            status_id=status_id
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_id",)
    assert "input should be a valid uuid" in error["msg"].lower()