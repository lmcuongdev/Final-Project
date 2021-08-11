import pytest
from flask_bcrypt import generate_password_hash

from app import app
from config.config import TestConfig
from models.user import UserModel
from models.item import ItemModel
from database import db
from helpers.auth import create_access_token


@pytest.fixture()
def client():
    # Setting up the application
    app.config['TESTING'] = True
    app.config.from_object(TestConfig)

    with app.test_client() as client:
        yield client

    # Clear database
    with app.app_context():
        ItemModel.query.delete()
        UserModel.query.delete()
        db.session.commit()


# fixture to seed users data
@pytest.fixture()
def seed_users():
    users = [
        {'id': 1, 'username': 'admin', 'password': generate_password_hash('password')},
        {'id': 2, 'username': 'user', 'password': generate_password_hash('password')},
    ]
    with app.app_context():
        db.session.add_all([UserModel(**user) for user in users])
        db.session.commit()

    return users


# fixture to seed items data
@pytest.fixture()
def seed_items(seed_users):
    items = [
        {'id': 1, 'name': 'item1', 'description': 'desc1', 'user_id': 1, 'category_id': 1},
        {'id': 2, 'name': 'item2', 'description': 'desc2', 'user_id': 2, 'category_id': 1},
        {'id': 3, 'name': 'item3', 'description': 'desc3', 'user_id': 2, 'category_id': 2},
        {'id': 4, 'name': 'item4', 'description': 'desc4', 'user_id': 2, 'category_id': 1},
        {'id': 5, 'name': 'none', 'description': 'desc5', 'user_id': 1, 'category_id': 3},
    ]
    with app.app_context():
        db.session.add_all([ItemModel(**item) for item in items])
        db.session.commit()

    return items


# fixture create a valid access token
@pytest.fixture()
def auth_user(seed_users):
    auth_user = seed_users[0].copy()
    auth_user['access_token'] = create_access_token(auth_user['id'])
    return auth_user