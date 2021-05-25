import pytest

from mysql_client.client import MySqlClient


@pytest.fixture(scope='session')
def mysql_client():
    my_sql_client = MySqlClient(user='test_qa', password='qa_test', db_name='TEST')
    my_sql_client.connect()
    yield my_sql_client
    my_sql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        my_sql_client = MySqlClient(user='test_qa', password='qa_test', db_name='TEST')
        my_sql_client.recreate_db()
        my_sql_client.connect()
        # Создание таблиц
        my_sql_client.create_table_test_users()
        my_sql_client.connection.close()
