from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
result = Table('result', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('match_id', Integer),
    Column('result_a', Integer),
    Column('result_b', Integer),
)

results = Table('results', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('match_id', Integer),
    Column('set_id', Integer),
    Column('result_a', Integer),
    Column('result_b', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['result'].drop()
    post_meta.tables['results'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['result'].create()
    post_meta.tables['results'].drop()
