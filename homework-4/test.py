import pytest
from base_test import BaseCase


class TestMarusya(BaseCase):
    @pytest.mark.AndroidUI
    def test_question(self):
        article_title = '146 млн.'
        self.main_page.send_question('Russia')
        self.main_page.get_article('Россия')
        self.main_page.swipe_from_to_target_and_click(from_btn='Нет',
                                                      target_btn='численность населения россии',
                                                      count_swipes=3)
        target_text = self.main_page.get_article(article_title)
        assert target_text == article_title, f'Error: check: {article_title}, target text: {target_text} '

    @pytest.mark.AndroidUI
    def test_math(self):
        expression = '3 + 3'
        result = '6'
        self.main_page.send_question(expression)
        answer = self.main_page.get_dialog_answer()
        assert result == answer, f'Error: check: {result}, answer: {answer} '

    @pytest.mark.AndroidUI
    def test_news(self):
        source = 'Вести FM'
        track_name = 'Вести ФМ'

        self.setting_page = self.main_page.go_to_settings()
        self.news_page = self.setting_page.click_to_news_sources()
        assert self.news_page.select_source(source=source), f'Error: {source} is not selected'

        self.news_page.return_to_main_page(taps=2)
        self.main_page.send_question('News')
        target_track = self.main_page.get_news_track_name()
        assert track_name == target_track, f'Error: check {track_name}, track {target_track}'

    @pytest.mark.AndroidUI
    def test_version(self):
        self.setting_page = self.main_page.go_to_settings()
        self.about_page = self.setting_page.click_to_about_app()

        file_name = self.config['apk']
        version = file_name.split('v')[-1].split('.apk')[0]
        target_version = self.about_page.get_version()
        assert version == target_version, f'ERROR version:{version}, target_version:{target_version}'

        phrase = "Все права защищены"
        copyright_text = self.about_page.get_copyright()
        assert phrase in copyright_text, f'ERROR phrase:{phrase}, about_text:{copyright_text}'