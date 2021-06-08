import sqlalchemy
from sqlalchemy import inspect
from sqlalchemy.orm import sessionmaker
from sqlalchemy.orm.exc import ObjectDeletedError

from mysql_client.models import Base, TestUsers


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

    def create_table_test_users(self):
        if not inspect(self.engine).has_table('test_users'):
            Base.metadata.tables['test_users'].create(self.engine)

    def delete_user(self, **kwargs):
        self.session.query(TestUsers).filter_by(**kwargs).delete()

    def clear_all_users(self, mysql_users=None, test_users=None):  # Deleting all users
        # TODO Исправить
        if mysql_users is not None:
            for user in mysql_users:
                try:
                    self.delete_user(username=user.username)
                except ObjectDeletedError:
                    pass
        if test_users is not None:
            for user in test_users:
                try:
                    self.delete_user(username=user.username)
                except ObjectDeletedError:
                    pass

    def get_user(self, **kwargs):
        self.session.commit()
        user = self.session.query(TestUsers).filter_by(**kwargs).first()
        return user

    def get_users(self, **kwargs):
        self.session.commit()
        users = self.session.query(TestUsers).filter_by(**kwargs).all()
        return users

    def check_exist_user(self, **kwargs):
        self.session.commit()
        exist = self.session.query(self.session.query(TestUsers).filter_by(**kwargs).exists()).scalar()
        return exist
