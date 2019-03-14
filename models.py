import os

from peewee import SqliteDatabase, Model, IntegerField, CompositeKey, ForeignKeyField

from config import BASE_DIR

db = SqliteDatabase(os.path.join(BASE_DIR, 'db.sqlite3'), pragmas={
    'journal_mode': 'wal',
    'cache_size': 10000,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})


class WhiteList(Model):
    user_id = IntegerField(null=False, unique=True)
    group_id = ForeignKeyField('Group', 'group_id')

    class Meta:
        database = db
        primary_key = CompositeKey('user_id')


class BlackList(Model):
    user_id = IntegerField(null=False, unique=True)

    class Meta:
        database = db
        primary_key = CompositeKey('user_id')


class Group(Model):
    group_id = IntegerField(null=False, unique=True)
    admin_group_id = IntegerField(null=False, unique=True)

    class Meta:
        database = db
        primary_key = CompositeKey('group_id')
