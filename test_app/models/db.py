import enum
from datetime import datetime

from sqlalchemy import (
    MetaData,
    Table,
    Enum,
    Column,
    ForeignKey,
    Integer,
    String,
    DateTime,
)


meta = MetaData()


class Role(enum.Enum):
    """
    VALUES (1, 'admin'), (2, 'manager'), (3, 'user');
    """
    admin = 1
    manager = 2
    user = 3


accounts = Table(
    'accounts', meta,

    Column('id', Integer, primary_key=True),
    Column('first_name', String(200), nullable=True),
    Column('last_name', String(200), nullable=True),
    Column('email', String(355), nullable=False),
    Column('date_created', DateTime, nullable=False, default=datetime.now),
    Column('date_edited', DateTime, nullable=False, default=datetime.now),
    Column('role', Enum(Role), default=Role.user.value),
)


carts = Table(
    'carts', meta,

    Column('id', Integer, primary_key=True),
    Column('order_id', Integer, ForeignKey('orders.id')),
    Column('product_id', Integer, ForeignKey('products.id')),
)


orders = Table(
    'orders', meta,

    Column('id', Integer, primary_key=True),
    Column('date_created', DateTime, nullable=False, default=datetime.now),
    Column('date_edited', DateTime, nullable=False, default=datetime.now),
    Column('account_id', Integer, ForeignKey('accounts.id', ondelete='CASCADE')),
)


products = Table(
    'products', meta,

    Column('id', Integer, primary_key=True),
    Column('name', String(200), nullable=False),
    Column('price', Integer, nullable=False),
    Column('date_created', DateTime, nullable=False, default=datetime.now),
    Column('date_edited', DateTime, nullable=False, default=datetime.now),
)
