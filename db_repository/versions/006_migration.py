from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
person = Table('person', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('first_name', String(length=255), nullable=False),
    Column('last_name', String(length=255), nullable=False),
    Column('address_line1', String(length=255)),
    Column('address_line2', String(length=255)),
    Column('address_city', String(length=255)),
    Column('address_state', String(length=2)),
    Column('address_postal_code', String(length=30)),
    Column('address_country', String(length=3)),
    Column('birthdate', DateTime),
    Column('sex', String(length=15)),
    Column('case_id', Integer),
    Column('role_id', Integer),
    Column('role_comment', String(length=127)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['person'].columns['role_id'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['person'].columns['role_id'].drop()
