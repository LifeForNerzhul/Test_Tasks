import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By


@pytest.fixture(scope='session')
def firefox_browser():
    browser = webdriver.Firefox()
    browser.implicitly_wait(2)
    yield browser
    browser.quit()


class TestYandexSearch:
    def test_first_result_contain_query(self, firefox_browser):
        self.key_word = 'Selenium'
        # Переходим на ya.ru
        firefox_browser.get('https://ya.ru')
        # Находим поле ввода
        self.input_field = firefox_browser.find_element(By.ID, 'text')
        # Передаём в поле ввода искомое слово и отправляем
        self.input_field.send_keys(self.key_word)
        self.input_field.submit()
        # Находим первый результат поисковой выдачи
        self.res = firefox_browser.find_element(By.ID, 'search-result')
        self.res = self.res.find_element(By.TAG_NAME, 'li').text

        assert self.key_word in self.res
