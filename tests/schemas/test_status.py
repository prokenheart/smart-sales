import pytest
from app.schemas.status import StatusBase
from pydantic import ValidationError

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

#Thiếu status_name
def test_status_base_missing_status_name():
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(
            status_code="UNPAID"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_name",)
    assert error["type"] == "missing"

#Thiếu status_code
def test_status_base_missing_status_code():
    with pytest.raises(ValidationError) as exc_info:
        StatusBase(
            status_name="Unpaid"
        )
    error = exc_info.value.errors()[0]

    assert error["loc"] == ("status_code",)
    assert error["type"] == "missing"    