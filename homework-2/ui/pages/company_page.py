import allure

from ui.pages.base_page import BasePage
from ui.locators.page_locators import CompanyPageLocators
from selenium.common.exceptions import TimeoutException


class CompanyPage(BasePage):   # Страницы Рекламные компании
    locators = CompanyPageLocators()
    url = "https://target.my.com/dashboard"

    def is_present(self, locator):
        try:
            self.find_visible(locator, timeout=5)
            result = True
        except TimeoutException:
            result = False
        return result

    @allure.step('Creating company {target}, {file}, {url}, {name}')
    def create_company(self, target, file, url, name):  # Метод создания компании
        if self.is_present(self.locators.TITLE_INSTR_COMPANY):
            self.click(self.locators.BTN_CREATE1_COMPANY)
        else:
            self.click(self.locators.BTN_CREATE2_COMPANY)

        self.click((self.locators.BTN_TARGET_COMPANY[0],
                    self.locators.BTN_TARGET_COMPANY[1].format(target)))
        self.send_data(self.locators.INPUT_URL_COMPANY, url)
        self.send_data(self.locators.INPUT_NAME_COMPANY, name)
        self.click(self.locators.BTN_ADV_TYPE_COMPANY)
        self.find_located(self.locators.INP_UPD_IMG_COMPANY).send_keys(file)
        self.click(self.locators.BTN_SAVE_COMPANY)

        company_names = self.finds(self.locators.LINKS_COMPANY)
        company_names = [c.text for c in company_names]
        return name, company_names

