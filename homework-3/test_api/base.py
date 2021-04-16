import pytest
import config
import faker

fake = faker.Faker()


class ApiBase:  # Базовый класс тестов API
    authorize = True

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        if self.authorize:
            self.api_client.post_auth(config.LOGIN, config.PASSWORD)

    def create_segment(self, name, pass_condition, obj_type):  # Метод создания сегмента
        response = self.api_client.post_create_segment(name=name, pass_condition=pass_condition, object_type=obj_type)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response['name'] == name
        assert json_response.get('id')
        return json_response['id']

    def check_segment(self, segment_id, exp_status):  # Метод проверки присутствия сегмента
        response = self.api_client.get_check_segment(segment_id=segment_id)
        assert response.status_code == exp_status

    def random_text(self, count):
        return fake.lexify(text='?'*count)

    def delete_segment(self, segment_id):  # Метод удаления сегмента
        response = self.api_client.post_delete_segment(segment_id=segment_id)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('successes')
        return json_response['successes'][0]['source_id']

