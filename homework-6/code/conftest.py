import pytest

from mysql.client import MySqlClient


@pytest.fixture(scope='session')
def mysql_client():
    my_sql_client = MySqlClient(user='root', password='pass', db_name='TEST_SQL')
    my_sql_client.connect()
    yield my_sql_client
    my_sql_client.connection.close()


def pytest_configure(config):
    if not hasattr(config, 'workerinput'):
        my_sql_client = MySqlClient(user='root', password='pass', db_name='TEST_SQL')
        my_sql_client.recreate_db()
        my_sql_client.connect()
        my_sql_client.create_table_count_requests()
        my_sql_client.create_table_typed_requests()
        my_sql_client.create_table_biggest_requests()
        my_sql_client.create_table_user_frequent_requests()
        my_sql_client.create_table_url_frequent_requests()
        my_sql_client.connection.close()
