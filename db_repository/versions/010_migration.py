from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
case__status = Table('case__status', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('description', String(length=255)),
)

case = Table('case', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date_opened', DateTime),
    Column('date_closed', DateTime),
    Column('date_updated', DateTime),
    Column('case_name', String(length=255)),
    Column('court_case_number', String(length=255)),
    Column('court_name', String(length=255)),
    Column('case_status_id', Integer),
    Column('notes', Text),
)

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
    Column('phone_number', String(length=28)),
    Column('birthdate', DateTime),
    Column('sex', String(length=15)),
    Column('case_id', Integer),
    Column('role_id', Integer),
    Column('role_comment', String(length=127)),
    Column('notes', Text),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['case__status'].create()
    post_meta.tables['case'].columns['case_status_id'].create()
    post_meta.tables['case'].columns['court_name'].create()
    post_meta.tables['case'].columns['date_updated'].create()
    post_meta.tables['case'].columns['notes'].create()
    post_meta.tables['person'].columns['notes'].create()
    post_meta.tables['person'].columns['phone_number'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['case__status'].drop()
    post_meta.tables['case'].columns['case_status_id'].drop()
    post_meta.tables['case'].columns['court_name'].drop()
    post_meta.tables['case'].columns['date_updated'].drop()
    post_meta.tables['case'].columns['notes'].drop()
    post_meta.tables['person'].columns['notes'].drop()
    post_meta.tables['person'].columns['phone_number'].drop()
