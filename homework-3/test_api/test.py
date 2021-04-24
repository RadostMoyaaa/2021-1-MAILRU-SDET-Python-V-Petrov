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
    def test_campaign(self, campaign):
        campaign_id = campaign
        self.check_campaign_status(campaign_id=campaign_id, status="NO_ALLOWED_BANNERS")