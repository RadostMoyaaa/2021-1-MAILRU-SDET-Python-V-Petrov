import os

import pytest
import config
import faker

fake = faker.Faker()


class ApiBase:  # Базовый класс тестов API
    authorize = True
    LOGIN = config.LOGIN
    PASSWORD = config.PASSWORD
    image_data = {'directory': None,
                  'name': None}

    @pytest.fixture(scope='function', autouse=True)
    def setup(self, api_client):
        self.api_client = api_client
        if self.authorize:
            self.api_client.post_auth(self.LOGIN, self.PASSWORD)

    def create_segment(self, name, pass_condition, obj_type):
        response = self.api_client.post_create_segment(name=name, pass_condition=pass_condition, object_type=obj_type)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response['name'] == name
        return json_response['id']

    def check_segment(self, segment_id, exp_status):
        response = self.api_client.get_check_segment(segment_id=segment_id)
        assert response.status_code == exp_status

    def random_text(self, count):
        return fake.lexify(text='?'*count)

    def delete_segment(self, segment_id):
        response = self.api_client.post_delete_segment(segment_id=segment_id)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('successes')
        return json_response['successes'][0]['source_id']

    def upload_image(self, file):
        response = self.api_client.post_upload_image(file=file)
        assert response.status_code == 200
        json_response = response.json()
        assert json_response.get('id')
        return json_response['id']

    def get_url_id(self, target_url):
        response = self.api_client.get_id_url(target_url=target_url)
        assert response.status_code == 200
        json_response = response.json()
        return json_response['id']

    def create_campaign(self, name, image_id, url_id):
        response = self.api_client.post_create_campaign(name=name, image_id=image_id, url_id=url_id)
        assert response.status_code == 200
        json_response = response.json()
        return json_response['id']

    def check_campaign_status(self, campaign_id, status):
        response = self.api_client.get_campaign_status(campaign_id=campaign_id)
        json_response = response.json()
        assert json_response.get('issues')[0]['code'] == status

    def delete_campaign(self, campaign_id):
        response = self.api_client.delete_campaign(campaign_id=campaign_id)
        assert response.status_code == 204
        self.check_campaign_status(campaign_id=campaign_id, status='ARCHIVED')

    @pytest.fixture()
    def campaign(self, repo_root):
        url_id = self.get_url_id(fake.url())
        file = os.path.join(repo_root, 'test_api', 'testImg2.jpg')
        image_id = self.upload_image(file)
        campaign_id = self.create_campaign(name=self.random_text(5), image_id=image_id, url_id=url_id)

        yield campaign_id

        self.delete_campaign(campaign_id=campaign_id)