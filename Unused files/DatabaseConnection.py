import psycopg2
from psycopg2.extras import DictCursor


class DatabaseConnection:
    __instance = None

    def __new__(cls, *args, **kwargs):
        if cls.__instance is None:
            cls.__instance = super(DatabaseConnection, cls).__new__(cls)
        return cls.__instance

    def __init__(self, db_name, user, password, host='localhost', port='5432'):
        if not hasattr(self, 'connection'):
            self.connection = psycopg2.connect(
                dbname=db_name,
                user=user,
                password=password,
                host=host,
                port=port
            )
            self.cursor = self.connection.cursor(cursor_factory=DictCursor)

    def execute(self, query, params=None):
        self.cursor.execute(query, params)

    def fetchone(self):
        return self.cursor.fetchone()

    def fetchall(self):
        return self.cursor.fetchall()

    def commit(self):
        self.connection.commit()

    def close(self):
        self.cursor.close()
        self.connection.close()