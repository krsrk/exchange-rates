from peewee import MySQLDatabase


class OrmEngine:
    engine = MySQLDatabase(
            'stock',
            user="root",
            password="root",
            host="db",
            port=3306
        )

    def __init__(self):
        pass

    def init_database(self):
        self.engine.init(self.engine)

    def get_engine(self):
        return self.engine

    def connect(self):
        return self.engine.connect()

    def is_connection_closed(self):
        return self.engine.is_closed()

    def close_connection(self):
        return self.engine.close()

    def migrate(self, model):
        return self.engine.create_tables([model])
