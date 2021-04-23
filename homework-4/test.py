import pytest
from _pytest.fixtures import FixtureRequest
from pages.main_page import MainPage


class BaseCase:
    @pytest.fixture(scope='function', autouse=True)
    def setup(self, request: FixtureRequest):
        self.main_page: MainPage = request.getfixturevalue('main_page')


class TestMarusya(BaseCase):
    def test_question(self):
        self.main_page.send_question('Russia')
        self.main_page.check_article('Россия')
        self.main_page.swipe_from_to_target_and_click(from_btn='Нет',
                                                      target_btn='численность населения россии',
                                                      count_swipes=3)
        self.main_page.check_article('146 млн.')

    def test_math(self):
        expression = '3 + 3'
        result = '6'
        self.main_page.send_question(expression)
        self.main_page.check_dialog_answer(result)

    def test_news(self):
        source = 'Вести FM'
        track_name = 'Вести ФМ'
        self.setting_page = self.main_page.go_to_settings()
        self.news_page = self.setting_page.click_to_news_sources()
        self.news_page.select_source(source=source)
        self.news_page.return_to_main_page(taps=2)
        self.main_page.send_question('News')
        self.main_page.check_news_track_name(check=track_name)