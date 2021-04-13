import os

import allure
import pytest

from base_tests.base import BaseCase
import config


class TestNegativeAuth(BaseCase):
    auto_login = False

    @pytest.mark.ui
    def test_auth_1(self):
        self.logger.info('Going to target.my.com, trying to login')

        with allure.step(f'First negative login cred\'s: {self.login_page.LOGIN, self.login_page.PASSWORD}'):
            self.login_page.change_creds(config.LOGIN, '')
            self.login_page.login()
            url = self.login_page.get_current_url()
            assert url != 'https://target.my.com/dashboard'

    @pytest.mark.ui
    def test_auth_2(self):
        self.logger.info('Going to target.my.com, trying to login')

        with allure.step(f'Second negative login cred\'s: {self.login_page.LOGIN, self.login_page.PASSWORD}'):
            self.login_page.change_creds(config.LOGIN, config.PASSWORD.upper())
            self.login_page.login()
            url = self.login_page.get_current_url()
            assert url != 'https://target.my.com/dashboard'


class TestSegments(BaseCase):

    @pytest.mark.ui
    def test_add_segment(self):
        self.logger.info(f'Going to segments, trying to create segment')

        with allure.step(f'Creating segment...'):
            segments_page = self.dashboard_page.go_to_segments()
            segment_id = segments_page.create_segment(name=segments_page.random_text(5))
            segments_page.driver.refresh()
            segments_id_list = segments_page.get_segments_id_list()

        with allure.step(f'Checking "{segment_id}" in {segments_id_list}'):
            assert segment_id in segments_id_list

    @pytest.mark.ui
    def test_delete_segment(self):
        self.logger.info(f'Going to segments, trying to create and delete segment')

        with allure.step(f'Creating and deleting segment...'):
            segments_page = self.dashboard_page.go_to_segments()
            segment_id = segments_page.create_segment(name=segments_page.random_text(5))
            segments_page.driver.refresh()
            segments_page.delete_segment(segment_id)
            segments_id_list = segments_page.get_segments_id_list()

        with allure.step(f'Checking created and deleted "{segment_id}" in {segments_id_list}'):
            assert segment_id not in segments_id_list


class TestCompany(BaseCase):

    @pytest.mark.ui
    def test_create_company(self, repo_root):
        self.logger.info(f'Going to company, trying to create company')

        with allure.step(f'Creating adv company...'):
            file = os.path.join(repo_root, 'ui', 'testImg.jpg')
            company_page = self.dashboard_page.go_to_company()
            name, company_names = company_page.create_company('Охват', file, "https://bethesda.net/ru/game/doom",
                                                              company_page.random_text(5))

        with allure.step(f'Checking created "{name}" in {company_names}'):
            assert name in company_names
