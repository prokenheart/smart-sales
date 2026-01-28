
from app.services import customer as service
from app.models import Customer
import pytest
from unittest.mock import patch, MagicMock
import uuid
from app.services.customer import DuplicateEmailError
from sqlalchemy.exc import IntegrityError

@pytest.fixture
def new_customer():
    return Customer(
        customer_name="Alice Peterson",
        customer_email="alice.peterson@gmail.com",
        customer_phone="+12025550107"
    )

@pytest.fixture
def existing_customer():
    return Customer(
        customer_id=uuid.uuid4(),
        customer_name="Bob Peterson",
        customer_email="Bob.peterson@gmail.com",
        customer_phone="+12025550108"
    )

@pytest.fixture
def existing_customer_2():
    return Customer(
        customer_id=uuid.uuid4(),
        customer_name="Charlie Peterson",
        customer_email="Charlie.peterson@gmail.com",
        customer_phone="+12025550109"
    )


def test_create_customer(mock_session, new_customer):
    with patch(
        "app.services.customer.get_customer_by_email",
        return_value=None
    ):
        created_customer = service.create_customer(
            mock_session,
            customer_name=new_customer.customer_name,
            customer_email=new_customer.customer_email,
            customer_phone=new_customer.customer_phone
        )

    mock_session.add.assert_called_once()
    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert created_customer.customer_name == new_customer.customer_name
    assert created_customer.customer_email == new_customer.customer_email
    assert created_customer.customer_phone == new_customer.customer_phone

def test_create_customer_integrity_error(mock_session, new_customer):
    with patch(
        "app.services.customer.get_customer_by_email",
        return_value=None
    ):
        mock_session.commit.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=None
        )

        with pytest.raises(DuplicateEmailError):
            service.create_customer(
                mock_session,
                customer_name=new_customer.customer_name,
                customer_email=new_customer.customer_email,
                customer_phone=new_customer.customer_phone
            )

    mock_session.rollback.assert_called_once()

def test_create_customer_email_exists(mock_session, new_customer, existing_customer):
    with patch(
        "app.services.customer.get_customer_by_email",
        return_value=existing_customer
    ):
        with pytest.raises(DuplicateEmailError, match="Email already exists"):
            service.create_customer(
                mock_session,
                customer_name=new_customer.customer_name,
                customer_email=new_customer.customer_email,
                customer_phone=new_customer.customer_phone
            )

def test_get_customer(mock_session, existing_customer):
    mock_session.execute.return_value.scalar_one_or_none.return_value = existing_customer

    customer = service.get_customer(
        mock_session,
        customer_id=existing_customer.customer_id
    )

    mock_session.execute.assert_called_once()
    assert customer is existing_customer

def test_get_customer_not_found(mock_session):
    mock_session.execute.return_value.scalar_one_or_none.return_value = None

    customer = service.get_customer(
        mock_session,
        customer_id=uuid.uuid4()
    )

    mock_session.execute.assert_called_once()
    assert customer is None

def test_get_customer_by_email(mock_session, existing_customer):
    mock_session.execute.return_value.scalar_one_or_none.return_value = existing_customer

    customer = service.get_customer_by_email(
        mock_session,
        customer_email=existing_customer.customer_email
    )

    mock_session.execute.assert_called_once()
    assert customer is existing_customer

def test_get_customer_by_email_not_found(mock_session):
    mock_session.execute.return_value.scalar_one_or_none.return_value = None

    customer = service.get_customer_by_email(
        mock_session,
        customer_email='alice.peterson@gmail.com'
    )
    mock_session.execute.assert_called_once()
    assert customer is None

def test_get_all_customers(mock_session, existing_customer):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [existing_customer]

    customers = service.get_all_customers(mock_session)

    mock_session.execute.assert_called_once()
    assert customers == [existing_customer]

def test_get_all_customers_empty(mock_session):
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    customers = service.get_all_customers(mock_session)

    mock_session.execute.assert_called_once()
    assert customers == []

def test_update_customer(mock_session, existing_customer, new_customer):
    with(
        patch(
            "app.services.customer.get_customer",
            return_value=existing_customer
        ),
        patch(
            "app.services.customer.get_customer_by_email",
            return_value=None
        )
    ):
        updated_customer = service.update_customer(
            mock_session,
            customer_id=existing_customer.customer_id,
            customer_name=new_customer.customer_name,
            customer_email=new_customer.customer_email,
            customer_phone=new_customer.customer_phone
        )

    mock_session.commit.assert_called_once()
    mock_session.refresh.assert_called_once()
    assert updated_customer is existing_customer

def test_update_customer_not_found(mock_session, new_customer):
    with patch(
        "app.services.customer.get_customer",
        return_value=None
    ):
        updated_customer = service.update_customer(
            mock_session,
            customer_id=uuid.uuid4(),
            customer_name=new_customer.customer_name,
            customer_email=new_customer.customer_email,
            customer_phone=new_customer.customer_phone
        )

    assert updated_customer is None

def test_update_customer_email_exists(mock_session, existing_customer, existing_customer_2):
    with (
        patch(
            "app.services.customer.get_customer",
            return_value=existing_customer
        ),
        patch(
            "app.services.customer.get_customer_by_email",
            return_value=existing_customer_2
        )
    ):
        with pytest.raises(DuplicateEmailError, match="Email already exists"):
            service.update_customer(
                mock_session,
                customer_id=existing_customer.customer_id,
                customer_email=existing_customer_2.customer_email
            )

def test_update_customer_integrity_error(mock_session, existing_customer, new_customer):
    with (
        patch(
            "app.services.customer.get_customer",
            return_value=existing_customer
        ),
        patch(
            "app.services.customer.get_customer_by_email",
            return_value=None
        )
    ):
        mock_session.commit.side_effect = IntegrityError(
            statement=None,
            params=None,
            orig=None
        )

        with pytest.raises(DuplicateEmailError):
            service.update_customer(
                mock_session,
                customer_id=existing_customer.customer_id,
                customer_name=new_customer.customer_name,
                customer_email=new_customer.customer_email,
                customer_phone=new_customer.customer_phone
            )

    mock_session.rollback.assert_called_once()

def test_delete_customer(mock_session, existing_customer):
    with patch(
        "app.services.customer.get_customer",
        return_value=existing_customer
    ):
        deleted_id = service.delete_customer(
            mock_session,
            customer_id=existing_customer.customer_id
        )

    mock_session.delete.assert_called_once_with(existing_customer)
    mock_session.commit.assert_called_once()
    assert deleted_id == existing_customer.customer_id

def test_delete_customer_not_found(mock_session):
    with patch(
        "app.services.customer.get_customer",
        return_value=None
    ):
        deleted_id = service.delete_customer(
            mock_session,
            customer_id=uuid.uuid4()
        )

    assert deleted_id is None

def search_customers_by_name(mock_session, existing_customer, existing_customer_2):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        existing_customer,
        existing_customer_2
    ]

    customers = service.search_customers_by_name(
        mock_session,
        name_query="Perterson"
    )

    mock_session.execute.assert_called_once()
    assert customers == [existing_customer, existing_customer_2]

def test_search_customers_by_name_no_results(mock_session):
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    customers = service.search_customers_by_name(
        mock_session,
        name_query="Nonexistent"
    )

    mock_session.execute.assert_called_once()
    assert customers == []

def test_search_customers_by_email(mock_session, existing_customer):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        existing_customer
    ]

    customers = service.search_customers_by_email(
        mock_session,
        email_query="bob.peterson@"
    )

    mock_session.execute.assert_called_once()
    assert customers == [existing_customer]

def test_search_customers_by_email_no_results(mock_session):
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    customers = service.search_customers_by_email(
        mock_session,
        email_query="nonexistent@"
    )

    mock_session.execute.assert_called_once()
    assert customers == []

def test_search_customers_by_phone(mock_session, existing_customer):
    mock_session.execute.return_value.scalars.return_value.all.return_value = [
        existing_customer
    ]

    customers = service.search_customers_by_phone(
        mock_session,
        phone_query="+12025550108"
    )

    mock_session.execute.assert_called_once()
    assert customers == [existing_customer]

def test_search_customers_by_phone_no_results(mock_session):
    mock_session.execute.return_value.scalars.return_value.all.return_value = []

    customers = service.search_customers_by_phone(
        mock_session,
        phone_query="+19999999999"
    )

    mock_session.execute.assert_called_once()
    assert customers == []