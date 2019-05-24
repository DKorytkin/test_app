from test_app.models.db import Role, accounts, products

from tests.service import fake


def _create_user(role) -> dict:
    params = {
        'first_name': fake.first_name(),
        'last_name': fake.last_name(),
        'email': fake.email(),
        'role': role,
    }
    return accounts.insert().values(**params)


def user() -> dict:
    return _create_user(Role.user)


def user_admin() -> dict:
    return _create_user(Role.admin)


def user_manager() -> dict:
    return _create_user(Role.manager)


def product() -> dict:
    params = {
        'name': fake.word(),
        'price': fake.pyint(),
    }
    return products.insert().values(**params)
