from sqlalchemy import *
from migrate import *


from migrate.changeset import schema
pre_meta = MetaData()
post_meta = MetaData()
matches = Table('matches', pre_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
    Column('player_a', Integer),
    Column('player_b', Integer),
    Column('nr_sets', Integer),
    Column('group', String),
    Column('round', Integer),
)

matches = Table('matches', post_meta,
    Column('id', Integer, primary_key=True, nullable=False),
    Column('date', DateTime),
    Column('round', Integer),
    Column('pool', String(length=1)),
    Column('player_a', Integer),
    Column('player_b', Integer),
    Column('nr_sets', Integer),
)


def upgrade(migrate_engine):
    # Upgrade operations go here. Don't create your own engine; bind
    # migrate_engine to your metadata
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['matches'].columns['group'].drop()
    post_meta.tables['matches'].columns['pool'].create()


def downgrade(migrate_engine):
    # Operations to reverse the above upgrade go here.
    pre_meta.bind = migrate_engine
    post_meta.bind = migrate_engine
    pre_meta.tables['matches'].columns['group'].create()
    post_meta.tables['matches'].columns['pool'].drop()
