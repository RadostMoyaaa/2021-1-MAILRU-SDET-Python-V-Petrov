from base_mysql import MySqlBase
from mysql_client.models import TestUsers


class TestMySQL(MySqlBase):
    def test(self):
        user = self.mysql_builder.create_test_user()
        users = self.mysql.session.query(TestUsers).all()
        print(users)
