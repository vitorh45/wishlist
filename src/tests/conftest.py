import pytest
from flask_jwt_extended import create_access_token

from api.app import create_app, db
from api.application.persistency.tables import Product as ProductTable


@pytest.fixture(scope="package")
def app():
    app = create_app("Testing")
    app.config["TESTING"] = True
    client = app.test_client()
    with app.app_context():
        yield client


@pytest.fixture(autouse=True)
def run_around_tests():
    yield
    db.session.rollback()


def pytest_addoption(parser):
    parser.addoption("--skip-startfinish", default=False, action="store_true")


@pytest.fixture
def skip_startfinish(request):
    return request.config.getoption("--skip-startfinish")


def pytest_sessionstart(session):
    from sqlalchemy import text, exc

    if session.config.getoption("--skip-startfinish"):
        return

    app = create_app("Testing")
    app.config["TESTING"] = True

    with app.app_context():
        db.metadata.bind = db.engine
        try:
            db.session.execute(text('CREATE EXTENSION IF NOT EXISTS "uuid-ossp"'))
        except exc.OperationalError:
            session.db_connected = False
        else:
            session.db_connected = True
            db.session.commit()
            db.create_all()


def pytest_sessionfinish(session):
    if session.config.getoption("--skip-startfinish") or not session.db_connected:
        return

    app = create_app("Testing")
    with app.app_context():
        db.metadata.bind = db.engine
        db.drop_all()


@pytest.fixture
def add_producs_db():
    product_1 = ProductTable(brand="Gibson", title="Les Paul 69 cherry sunburst", price=1500000, image="products/list/gibson_01.jpg")
    product_2 = ProductTable(brand="Gibson", title="Les Paul 67 goldtop", price=1700000, image="products/list/gibson_02.jpg")
    db.session.add_all([product_1, product_2])
    db.session.commit()
    return (product_1, product_2)


@pytest.fixture
def create_client_payload():
    return {
        "name": "John Wick 123",
        "email": "johnwick123@example.com"
    }


@pytest.fixture
def create_client_mapping(create_client_payload):
    from api.presentation.mappings import CreateClientRequestMapping

    return CreateClientRequestMapping(
        payload=create_client_payload
    )


@pytest.fixture
def update_client_payload():
    return {
        "name": "John Wick 123"
    }


@pytest.fixture
def update_client_mapping(update_client_payload):
    from api.presentation.mappings import UpdateClientRequestMapping

    return UpdateClientRequestMapping(
        payload=update_client_payload
    )


@pytest.fixture
def user_login_payload():
    return {
        "username": "johnwick",
        "password": "jardani"
    }


@pytest.fixture
def user_login_mapping(user_login_payload):
    from api.presentation.mappings import UserLoginRequestMapping

    return UserLoginRequestMapping(
        payload=user_login_payload
    )
    

@pytest.fixture
def create_wishlist_payload():
    return {
        "client_id": "7c35dad8-8f89-44e1-8c26-94e1ccbf14e1"
    }


@pytest.fixture
def create_wishlist_mapping(create_wishlist_payload):
    from api.presentation.mappings import CreateWishlistRequestMapping

    return CreateWishlistRequestMapping(
        payload=create_wishlist_payload
    )


@pytest.fixture
def add_product_payload():
    return {
        "product_id": "0075dad8-8f89-44e1-8c26-94e1ccbf14e1"
    }


@pytest.fixture
def add_product_mapping(add_product_payload):
    from api.presentation.mappings import AddProductWishlistRequestMapping

    return AddProductWishlistRequestMapping(
        payload=add_product_payload
    )


@pytest.fixture()
def create_jwt_user():
    return create_access_token(identity={"username": "user", "password": "user"})