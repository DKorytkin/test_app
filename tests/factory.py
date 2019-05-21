
from factory import Factory, Faker, SubFactory

from test_app.models.db import accounts, orders, Role


class MyFactory(Factory):

    @classmethod
    def _build(cls, model_class, *args, **kwargs):
        return model_class.insert().values(*args, **kwargs)


class AccountAdmin(MyFactory):

    class Meta:
        model = accounts

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    role = Role.admin


class AccountManager(MyFactory):

    class Meta:
        model = accounts

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    role = Role.manager


class AccountUser(MyFactory):

    class Meta:
        model = accounts

    first_name = Faker('first_name')
    last_name = Faker('last_name')
    email = Faker('email')
    role = Role.user


class UserOrder(MyFactory):

    class Meta:
        model = orders

    account_id = SubFactory(AccountUser)

