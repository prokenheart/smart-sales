from app.services import order as service
from app.models import Order, User, Customer, Status
import pytest
import uuid
from app.services.order import NotFoundError
from unittest.mock import patch
from datetime import date
from tests.conftest import MagicMock

@pytest.fixture
def existing_customer():
    return Customer(
        customer_id=uuid.uuid4()
    )

@pytest.fixture
def existing_user():
    return User(
        user_id=uuid.uuid4()
    )

@pytest.fixture
def default_status():
    return Status(
        status_id=uuid.uuid4(),
        status_name="Pending",
        status_code="PENDING"
    )

@pytest.fixture
def status():
    return Status(
        status_id=uuid.uuid4(),
        status_name="Completed",
        status_code="COMPLETED"
    )

@pytest.fixture
def new_order(existing_customer: Customer, existing_user: User):
    return Order(
        customer_id=existing_customer.customer_id,
        user_id=existing_user.user_id
    )

@pytest.fixture
def existing_order(existing_customer: Customer, existing_user: User):
    return Order(
        order_id=uuid.uuid4(),
        customer_id=existing_customer.customer_id,
        user_id=existing_user.user_id,
        status_id=uuid.uuid4()
    )

def test_create_order(mock_session: MagicMock, default_status: Status, existing_customer: Customer, existing_user: User, new_order: Order):
    with(
        patch(
            'app.services.order.get_customer',
            return_value=existing_customer
        ),
        patch(
            'app.services.order.get_user',
            return_value=existing_user
        ),
        patch(
            'app.services.order.get_default_status',
            return_value=default_status
        )
    ):
        order = service.create_order(
            db=mock_session,
            customer_id=new_order.customer_id,
            user_id=new_order.user_id
        )


    # Assert: DB actions
    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()

    # Assert: order object
    assert isinstance(order, Order)
    assert order.customer_id == new_order.customer_id
    assert order.user_id == new_order.user_id
    assert order.status_id == default_status.status_id

def test_create_order_customer_not_found(mock_session: MagicMock, existing_user: User):
    with patch(
        'app.services.order.get_customer',
        side_effect=NotFoundError("Customer with given ID does not exist.")
    ):
        with pytest.raises(NotFoundError) as exc_info:
            service.create_order(
                db=mock_session,
                customer_id=uuid.uuid4(),
                user_id=existing_user.user_id
            )
    assert str(exc_info.value) == "Customer with given ID does not exist."

def test_create_order_user_not_found(mock_session: MagicMock, existing_customer: Customer):
    with patch(
        'app.services.order.get_user',
        side_effect=NotFoundError("User with given ID does not exist.")
    ):
        with pytest.raises(NotFoundError) as exc_info:
            service.create_order(
                db=mock_session,
                customer_id=existing_customer.customer_id,
                user_id=uuid.uuid4()
            )
    assert str(exc_info.value) == "User with given ID does not exist."

def test_get_order(mock_session: MagicMock, existing_order: Order):
    mock_session.execute.return_value.scalar_one_or_none.return_value = existing_order

    order = service.get_order(
        db=mock_session,
        order_id=existing_order.order_id
    )

    mock_session.execute.assert_called_once()
    assert order == existing_order

def test_get_order_not_found(mock_session: MagicMock):
    mock_session.execute.return_value.scalar_one_or_none.return_value = None

    order = service.get_order(
        db=mock_session,
        order_id=uuid.uuid4()
    )

    mock_session.execute.assert_called_once()
    assert order is None

def test_get_orders_by_user(mock_session: MagicMock, existing_user: User, existing_order: Order):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [existing_order]

    with patch(
        'app.services.order.user_exists',
        return_value=True
    ):
        orders = service.get_orders_by_user(
            db=mock_session,
            user_id=existing_user.user_id
        )

    mock_session.execute.assert_called_once()
    assert orders == [existing_order]

def test_get_orders_by_user_not_found(mock_session: MagicMock):
    with patch(
        'app.services.order.user_exists',
        return_value=False
    ):
        with pytest.raises(NotFoundError) as exc_info:
            service.get_orders_by_user(
                db=mock_session,
                user_id=uuid.uuid4()
            )
    assert str(exc_info.value) == "User with given ID does not exist."

def test_get_orders_by_customer(mock_session: MagicMock, existing_customer: Customer, existing_order: Order):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [existing_order]

    with patch(
        'app.services.order.customer_exists',
        return_value=True
    ):
        orders = service.get_orders_by_customer(
            db=mock_session,
            customer_id=existing_customer.customer_id
        )

    mock_session.execute.assert_called_once()
    assert orders == [existing_order]

def test_get_orders_by_customer_not_found(mock_session: MagicMock):
    with patch(
        'app.services.order.customer_exists',
        return_value=False
    ):
        with pytest.raises(NotFoundError) as exc_info:
            service.get_orders_by_customer(
                db=mock_session,
                customer_id=uuid.uuid4()
            )
    assert str(exc_info.value) == "Customer with given ID does not exist."

def test_get_orders_by_status(mock_session: MagicMock, status: Status, existing_order: Order):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [existing_order]

    with patch(
        'app.services.order.get_status_by_code',
        return_value=status
    ):
        orders = service.get_orders_by_status(
            db=mock_session,
            status_code=status.status_code
        )

    mock_session.execute.assert_called_once()
    assert orders == [existing_order]

def test_get_all_orders(mock_session: MagicMock, existing_order: Order):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [existing_order]

    orders = service.get_all_orders(
        db=mock_session
    )

    mock_session.execute.assert_called_once()
    assert orders == [existing_order]

def test_update_order_status(mock_session: MagicMock, existing_order: Order, status: Status):
    with(
        patch('app.services.order.get_order', return_value=existing_order),
        patch('app.services.order.get_status', return_value=status)
    ):
        updated_order = service.update_order_status(
            db=mock_session,
            order_id=existing_order.order_id,
            status_id=status.status_id
        )

    assert updated_order.status_id == status.status_id
    mock_session.add.assert_called_once_with(existing_order)
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once_with(existing_order)

def test_update_order_status_not_found(mock_session: MagicMock):
    with patch('app.services.order.get_order', return_value=None):
        updated_order = service.update_order_status(
            db=mock_session,
            order_id=uuid.uuid4(),
            status_id=uuid.uuid4()
        )

    assert updated_order is None
    mock_session.add.assert_not_called()
    mock_session.commit.assert_not_called()
    mock_session.refresh.assert_not_called()

def test_delete_order(mock_session: MagicMock, existing_order: Order):
    with patch('app.services.order.get_order', return_value=existing_order):
        result = service.delete_order(
            db=mock_session,
            order_id=existing_order.order_id
        )

    assert result == existing_order.order_id
    mock_session.delete.assert_called_once_with(existing_order)
    mock_session.commit.assert_called_once()

def test_delete_order_not_found(mock_session: MagicMock):
    with patch('app.services.order.get_order', return_value=None):
        result = service.delete_order(
            db=mock_session,
            order_id=uuid.uuid4()
        )

    assert result is None
    mock_session.delete.assert_not_called()
    mock_session.commit.assert_not_called()

def test_get_user(mock_session: MagicMock, existing_user: User):
    mock_session.get.return_value = existing_user

    user = service.get_user(
        db=mock_session,
        user_id=existing_user.user_id
    )

    mock_session.get.assert_called_once_with(User, existing_user.user_id)
    assert user == existing_user

def test_get_user_not_found(mock_session: MagicMock):
    mock_session.get.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        service.get_user(
            db=mock_session,
            user_id=uuid.uuid4()
        )
    assert str(exc_info.value) == "User with given ID does not exist."

def test_get_customer(mock_session: MagicMock, existing_customer: Customer):
    mock_session.get.return_value = existing_customer

    customer = service.get_customer(
        db=mock_session,
        customer_id=existing_customer.customer_id
    )

    mock_session.get.assert_called_once_with(Customer, existing_customer.customer_id)
    assert customer == existing_customer

def test_get_customer_not_found(mock_session: MagicMock):
    mock_session.get.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        service.get_customer(
            db=mock_session,
            customer_id=uuid.uuid4()
        )
    assert str(exc_info.value) == "Customer with given ID does not exist."

def test_get_status(mock_session: MagicMock, status: Status):
    mock_session.get.return_value = status

    result_status = service.get_status(
        db=mock_session,
        status_id=status.status_id
    )

    mock_session.get.assert_called_once_with(Status, status.status_id)
    assert result_status == status

def test_get_status_not_found(mock_session: MagicMock):
    mock_session.get.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        service.get_status(
            db=mock_session,
            status_id=uuid.uuid4()
        )
    assert str(exc_info.value) == "Status with given ID does not exist."

def test_get_status_by_code(mock_session: MagicMock, status: Status):
    mock_session.execute.return_value.scalar_one_or_none.return_value = status

    result_status = service.get_status_by_code(
        db=mock_session,
        status_code=status.status_code
    )

    mock_session.execute.assert_called_once()
    assert result_status == status

def test_get_status_by_code_not_found(mock_session: MagicMock):
    mock_session.execute.return_value.scalar_one_or_none.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        service.get_status_by_code(
            db=mock_session,
            status_code="NON_EXISTENT_CODE"
        )
    assert str(exc_info.value) == "Status with given code does not exist."

def test_get_default_status(mock_session: MagicMock, default_status: Status):
    mock_session.execute.return_value.scalar_one_or_none.return_value = default_status

    result_status = service.get_default_status(
        db=mock_session
    )

    mock_session.execute.assert_called_once()
    assert result_status == default_status

def test_get_default_status_not_found(mock_session: MagicMock):
    mock_session.execute.return_value.scalar_one_or_none.return_value = None

    with pytest.raises(NotFoundError) as exc_info:
        service.get_default_status(
            db=mock_session
        )
    assert str(exc_info.value) == "Default status not found."

def test_user_exists(mock_session: MagicMock, existing_user: User):
    mock_session.execute.return_value.scalar.return_value = True

    exists = service.user_exists(
        db=mock_session,
        user_id=existing_user.user_id
    )

    mock_session.execute.assert_called_once()
    assert exists is True

def test_user_not_exists(mock_session: MagicMock):
    mock_session.execute.return_value.scalar.return_value = False

    exists = service.user_exists(
        db=mock_session,
        user_id=uuid.uuid4()
    )

    mock_session.execute.assert_called_once()
    assert exists is False

def test_customer_exists(mock_session: MagicMock, existing_customer: Customer):
    mock_session.execute.return_value.scalar.return_value = True

    exists = service.customer_exists(
        db=mock_session,
        customer_id=existing_customer.customer_id
    )

    mock_session.execute.assert_called_once()
    assert exists is True

def test_customer_not_exists(mock_session: MagicMock):
    mock_session.execute.return_value.scalar.return_value = False

    exists = service.customer_exists(
        db=mock_session,
        customer_id=uuid.uuid4()
    )

    mock_session.execute.assert_called_once()
    assert exists is False

def test_get_orders_by_date(mock_session: MagicMock, existing_order: Order):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        existing_order
    ]

    order_date = date(2026, 1, 28)

    result = service.get_orders_by_date(mock_session, order_date)

    assert result == [existing_order]

    mock_session.execute.assert_called_once()
    mock_session.execute.return_value.scalars.assert_called_once()
    mock_session.execute.return_value.scalars.return_value.all.assert_called_once()

