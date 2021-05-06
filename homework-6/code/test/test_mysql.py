import pytest


from mysql.builder import MySqlBuilder
from mysql.models import CountRequests, CountTyped, BiggestRequestsError
from mysql.log_parser import LogParser


class MySqlBase:

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mysql_client):
        self.mysql = mysql_client
        self.mysql_builder = MySqlBuilder(mysql_client)
        self.log_parser = LogParser(file_name='access.log', template="%a - - %t \"%r\" %s %b")


class TestMySqlLogs(MySqlBase):

    def test_count(self):
        requests_count = self.log_parser.get_count_of_requests()
        self.mysql_builder.create_count_requests(count=requests_count['Count'])
        assert len(self.mysql.session.query(CountRequests).all()) == len(requests_count)

    @pytest.mark.skip
    def test_typed_requests(self):
        typed_requests = self.log_parser.get_count_of_typed_requests()

        for k, v in typed_requests.items():
            self.mysql_builder.create_count_typed_request(name=k, count=v)

        assert len(self.mysql.session.query(CountTyped).all()) == len(typed_requests)

    @pytest.mark.skip
    def test_biggest_requests(self):
        biggest_requests = self.log_parser.get_biggest_requests()

        for r in biggest_requests:
            self.mysql_builder.create_biggest_request(*r)

        assert len(self.mysql.session.query(BiggestRequestsError).all()) == len(biggest_requests)
