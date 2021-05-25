import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from mysql_client.models import Base


class MySqlClient:
    def __init__(self, user, password, db_name):
        self.user = user
        self.password = password
        self.db_name = db_name
        self.host = 'mysql_container'
        self.port = 3306
        self.engine = None
        self.connection = None
        self.session = None

    def connect(self, db_created=True):
        db = self.db_name if db_created else ''

        self.engine = sqlalchemy.create_engine(
            f'mysql+pymysql://{self.user}:{self.password}@{self.host}:{self.port}/{db}'
        )

        self.connection = self.engine.connect()
        self.session = sessionmaker(bind=self.connection.engine)()

    def execute_query(self, query, fetch=True):
        res = self.connection.execute(query)
        if fetch:
            return res.fetchall()

    def recreate_db(self):
        self.connect(db_created=False)
        self.execute_query(f'DROP database if exists {self.db_name}', fetch=False)
        self.execute_query(f'CREATE database {self.db_name}', fetch=False)
        self.connection.close()

    def create_new_user(self):
        self.connect(db_created=True)  # Bad decision
        self.execute_query(f"CREATE USER 'test_qa' IDENTIFIED BY 'qa_test'", fetch=False)
        self.execute_query(f"GRANT ALL PRIVILEGES ON * . * to 'test_qa'", fetch=False)
        self.execute_query(f"FLUSH PRIVILEGES", fetch=False)
        self.connection.close()

    def create_table_test_users(self):
        if not inspect(self.engine).has_table('test_users'):
            Base.metadata.tables['test_users'].create(self.engine)
