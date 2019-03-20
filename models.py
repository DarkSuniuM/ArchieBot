import os

from peewee import SqliteDatabase, Model, IntegerField, CompositeKey, BooleanField

from config import BASE_DIR

db = SqliteDatabase(os.path.join(BASE_DIR, 'db.sqlite3'), pragmas={
    'journal_mode': 'wal',
    'cache_size': 10000,
    'foreign_keys': 1,
    'ignore_check_constraints': 0,
    'synchronous': 0
})


class User(Model):
    user_id = IntegerField(null=False, unique=False)
    group_id = IntegerField(null=False, unique=False)
    is_active = BooleanField(null=False, unique=False, default=False)

    class Meta:
        database = db
        primary_key = CompositeKey('user_id', 'group_id')
