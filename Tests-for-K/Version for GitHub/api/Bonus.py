import unittest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time


class MainPage:
    input_field = (By.TAG_NAME, "input")
    find_btn = (By.CSS_SELECTOR, 'button.flex')


class SimpleWidgetTestCase(unittest.TestCase):
    def setUp(self):
        self.options = webdriver.FirefoxOptions()
        self.options.set_preference('dom.webdriver.enabled', False)
        self.options.page_load_strategy = 'eager'
        self.driver = webdriver.Firefox(options=self.options)

    def test_basic(self):
        url = 'https://ipinfo.io/'

        self.driver.get(url)
        self.input_field = WebDriverWait(self.driver, 10).until(EC.presence_of_element_located(
            (MainPage.input_field[0], MainPage.input_field[1])))
        self.find_btn = self.driver.find_element(MainPage.find_btn[0], MainPage.find_btn[1])
        # Нужно дать время сайту заполнить поле ввода, если мы заполним поле до этого момента, то сайт
        # заменит наши данные на свои значения по умолчанию
        time.sleep(1)
        self.input_field.clear()
        self.input_field.send_keys("8.8.8.8")
        self.find_btn.click()

        assert self.driver.find_element(By.ID, 'ip-string').text.replace('\n', '') == 'ip:"8.8.8.8",'
        assert self.driver.find_element(By.ID, 'hostname-string').text.replace('\n', '') == 'hostname:"dns.google",'
        assert self.driver.find_element(By.ID, 'anycast-boolean').text.replace('\n', '') == 'anycast:true,'
        assert self.driver.find_element(By.ID, 'city-string').text.replace('\n', '') == 'city:"Mountain View",'
        assert self.driver.find_element(By.ID, 'region-string').text.replace('\n', '') == 'region:"California",'
        assert self.driver.find_element(By.ID, 'country-string').text.replace('\n', '') == 'country:"US",'
        assert self.driver.find_element(By.ID, 'loc-string').text.replace('\n', '') == 'loc:"37.4056,-122.0775",'
        assert self.driver.find_element(By.ID, 'org-string').text.replace('\n', '') == 'org:"AS15169 Google LLC",'
        assert self.driver.find_element(By.ID, 'postal-string').text.replace('\n', '') == 'postal:"94043",'
        assert self.driver.find_element(By.ID, 'timezone-string').text.replace('\n',
                                                                               '') == 'timezone:"America/Los_Angeles",'

    def tearDown(self):
        self.driver.quit()
