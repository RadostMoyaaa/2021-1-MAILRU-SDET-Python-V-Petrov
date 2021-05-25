import pytest
from mysql_client.builder import MySQLBuilder


class MySqlBase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySQLBuilder(mysql_client)
