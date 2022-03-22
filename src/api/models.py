from peewee import Model, UUIDField, CharField, TextField, IntegerField, DecimalField, DateTimeField
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


class ExchangeRate(Model):
    id = UUIDField(primary_key=True, index=True, unique=True)
    user_id = UUIDField(index=True)
    exchange_provider = CharField(max_length=50)
    exchange_rate = DecimalField()
    last_update = DateTimeField()

    class Meta:
        database = OrmEngine().get_engine()
        table_name = 'exchange_rates'
