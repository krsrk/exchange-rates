from peewee import Model, UUIDField, CharField, TextField, IntegerField
from orm.peewee import OrmEngine


class User(Model):
    id = UUIDField(primary_key=True, index=True, unique=True)
    username = CharField(max_length=150)
    email = CharField(max_length=150)
    password = TextField()
    request_limit = IntegerField()

    class Meta:
        database = OrmEngine().get_engine()
        table_name = 'users'
