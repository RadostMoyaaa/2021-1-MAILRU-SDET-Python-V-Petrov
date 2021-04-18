import os

import pytest
from faker import Faker

from test_api.base import ApiBase
fake = Faker()
SYMBOLS_COUNT = 10


class TestSegments(ApiBase):  # Тесты на создание и удаление сегмента

    @pytest.mark.api
    def test_create_segment(self):
        name = self.random_text(SYMBOLS_COUNT)
        created_id = self.create_segment(name=name, pass_condition=1, obj_type='remarketing_player')
        self.check_segment(segment_id=created_id, exp_status=200)

    @pytest.mark.api
    def test_delete_segment(self):
        name = self.random_text(SYMBOLS_COUNT)
        created_id = self.create_segment(name=name, pass_condition=1, obj_type='remarketing_player')
        self.check_segment(segment_id=created_id, exp_status=200)
        deleted_id = self.delete_segment(segment_id=created_id)
        self.check_segment(segment_id=deleted_id, exp_status=404)


class TestCampaigns(ApiBase):  # Тест на создание компании
    @pytest.mark.api
    def test_campaign(self, repo_root):
        url_id = self.get_url_id(fake.url())
        file = os.path.join(repo_root, 'test_api', 'testImg2.jpg')
        image_id = self.upload_image(file)
        campaign_id = self.create_campaign(name=self.random_text(5), image_id=image_id, url_id=url_id)
        self.delete_campaign(campaign_id=campaign_id)
