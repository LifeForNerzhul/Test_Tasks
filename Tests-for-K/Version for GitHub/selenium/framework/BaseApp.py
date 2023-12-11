from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class BasePage:

    def __init__(self, driver,
                 loc_product_name: str = '-------------------- for Networks',
                 loc_version: str = '3.0',
                 loc_block_name: str = 'About ----------------------- for Networks',
                 loc_sub_block_name: str = 'Hardware and software requirements',
                 loc_target: str = 'RAM: 4 GB, and an additional 2 GB for each monitoring point on this computer.'):
        self.driver = driver
        self.base_url = "https://support.--------.com/help/"
        self.loc_product_name = loc_product_name
        self.loc_version = loc_version
        self.loc_block_name = loc_block_name
        self.loc_sub_block_name = loc_sub_block_name
        self.loc_target = loc_target

    def find_element(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_element_located(locator),
                                                      message=f"Can't find element by locator {locator}")

    def find_elements(self, locator, time=10):
        return WebDriverWait(self.driver, time).until(EC.presence_of_all_elements_located(locator),
                                                      message=f"Can't find elements by locator {locator}")

    def go_to_site(self):
        return self.driver.get(self.base_url)
