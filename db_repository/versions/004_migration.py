from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
user = Table('user', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('username', String(length=50), nullable=False),
    Column('password', String(length=255), nullable=False),
    Column('reset_password_token', String(length=100), nullable=False),
    Column('email', String(length=255), nullable=False),
    Column('confirmed_at', DateTime),
    Column('is_active', Boolean, nullable=False),
    Column('first_name', String(length=100), nullable=False),
    Column('last_name', String(length=100), nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['user'].drop()
