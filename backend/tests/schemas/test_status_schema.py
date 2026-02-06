import pytest
from app.schemas.status import StatusBase, StatusIdPath, StatusCode
from pydantic import ValidationError
import uuid


# Basic valid case
def test_status_base_valid() -> None:
    status = StatusBase(status_name="Unpaid", status_code="UNPAID")
    assert status.status_name == "Unpaid"
    assert status.status_code == "UNPAID"


# Auto uppercase status_code
def test_status_base_upper() -> None:
    status = StatusBase(status_name="Unpaid", status_code="Unpaid")
    assert status.status_name == "Unpaid"
    assert status.status_code == "UNPAID"


# Invalid status_code format
@pytest.mark.parametrize("status_code", ["", "unpaid2", "unpaid@"])
def test_status_base_invalid_code(status_code: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(status_name="Unpaid", status_code=status_code)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert "only uppercase letters" in error["msg"].lower()


# Missing status_name
def test_status_base_missing_status_name() -> None:
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(status_code="UNPAID")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_name",)
    assert error["type"] == "missing"


# Missing status_code
def test_status_base_missing_status_code() -> None:
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(status_name="Unpaid")
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert error["type"] == "missing"


# Valid status_code
def test_status_code_valid() -> None:
    status = StatusCode(status_code="PAID")
    assert status.status_code == "PAID"


@pytest.mark.parametrize("status_code", ["", "paid2", "paid@"])
def test_status_code_invalid(status_code: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        StatusCode(status_code=status_code)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert "only uppercase letters" in error["msg"].lower()


# Valid status_id path
def test_status_id_path_valid() -> None:
    status_id = uuid.uuid4()
    status = StatusIdPath(status_id=status_id)
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
    ],
)
def test_status_id_path_invalid(status_id: str) -> None:
    with pytest.raises(ValidationError) as exc_info:
        StatusIdPath(status_id=status_id)
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_id",)
    assert "input should be a valid uuid" in error["msg"].lower()
