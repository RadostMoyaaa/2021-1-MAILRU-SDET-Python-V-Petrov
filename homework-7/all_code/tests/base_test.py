import pytest

from all_code.utils.builder import Builder


class BaseTest:

    def prepare(self):
        self.user = self.builder.create_user()

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, mock_client, logger):
        self.mock_client = mock_client
        self.logger = logger
        self.builder = Builder()
        self.prepare()

    def get_surname(self, name, expected_status):
        return self.mock_client.get_surname(name, expected_status)

    def put_update_user_surname(self, name, surname, expected_status):
        return self.mock_client.put_update_user_surname(name, surname, expected_status)

    def delete_user_surname(self, name, expected_status):
        self.mock_client.delete_user_surname(name, expected_status)
