from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
phone_log_entry = Table('phone_log_entry', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('timestamp', DateTime, nullable=False),
    Column('content', Text),
    Column('caller_id', Integer),
    Column('case_id', Integer, nullable=False),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['phone_log_entry'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    post_meta.tables['phone_log_entry'].drop()
