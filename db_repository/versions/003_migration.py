from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
person = Table('person', pre_meta,
    Column('id', INTEGER, primary_key=True, nullable=False),
    Column('first_name', VARCHAR(length=255), nullable=False),
    Column('last_name', VARCHAR(length=255), nullable=False),
    Column('address_line1', VARCHAR(length=255)),
    Column('address_line2', VARCHAR(length=255)),
    Column('address_city', VARCHAR(length=255)),
    Column('address_state', VARCHAR(length=2)),
    Column('address_postal_code', VARCHAR(length=30)),
    Column('address_country', VARCHAR(length=3)),
    Column('birthdate', DATETIME),
    Column('sex', VARCHAR(length=15)),
    Column('case_id', INTEGER),
    Column('role_id', INTEGER),
    Column('role_comment', VARCHAR(length=127)),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['role_id'].drop()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['person'].columns['role_id'].create()
