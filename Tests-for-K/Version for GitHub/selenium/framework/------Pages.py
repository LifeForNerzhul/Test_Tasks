from -------.NewFolder.framework.BaseApp import BasePage
from selenium.webdriver.common.by import By
import time


def search_elem(obj, locator: tuple):
    loc = locator[0]
    name = locator[1]
    return obj.find_element(loc, name)


def search_elems(obj, locator: tuple):
    loc = locator[0]
    name = locator[1]
    return obj.find_elements(loc, name)


class HelpLocators:
    loc_products = (By.CLASS_NAME, 'product')
    loc_dropdown = (By.CLASS_NAME, 'dropdown')
    loc_versions = (By.CLASS_NAME, 'dropdown__item')


class ProductLocators:
    loc_side_menu = (By.CLASS_NAME, 'aside__menu')
    loc_side_menu_blocks = (By.CLASS_NAME, 'contents__item ')
    loc_sub_blocks = (By.TAG_NAME, 'li')
    loc_page_version = (By.CLASS_NAME, 'dropdown__btn')
    loc_page_html = (By.TAG_NAME, 'html')
    loc_lang_dropdown = (By.CSS_SELECTOR, '.js_header_lang_list')
    loc_lang_dropdown_nemu = (By.CSS_SELECTOR, '.dropdown__list_opened')


class SearchHelper(BasePage):

    def help_page(self):
        products = self.find_elements(HelpLocators.loc_products)
        for product in products:
            html = product.get_attribute("outerHTML")
            if html.find(self.loc_product_name) != -1:
                dropdown_btn = search_elem(product, HelpLocators.loc_dropdown)
                dropdown_btn.click()
                versions = search_elems(dropdown_btn, HelpLocators.loc_versions)
                for version in versions:
                    html = version.get_attribute('outerHTML')
                    if html.find(self.loc_version) != -1:
                        version.click()
                        time.sleep(0.1)
                        return True
        raise Exception('На странице help не обнаружены запрашиваемые элементы')

    def product_page(self):
        side_block = self.find_element(ProductLocators.loc_side_menu)
        blocks = search_elems(side_block, ProductLocators.loc_side_menu_blocks)
        for block in blocks:
            html = block.get_attribute('outerHTML')
            if html.find(self.loc_block_name) != -1:
                block.click()
                sub_blocks = search_elems(block, ProductLocators.loc_sub_blocks)
                for sub_block in sub_blocks:
                    html = sub_block.get_attribute('outerHTML')
                    if html.find(self.loc_sub_block_name) != -1:
                        sub_block.click()
                        time.sleep(0.1)
                        return True
        raise Exception('На странице продукта не обнаружены запрашиваемые элементы')

    def check_target(self):
        html = self.find_element(ProductLocators.loc_page_html).text
        assert html.find(self.loc_target) != -1
        '''if html.find(self.loc_target) != -1:
            print('Нашли!')
        else:
            raise Exception("Текст не найден")'''

    def check_version(self):
        version = self.find_element(ProductLocators.loc_page_version).text
        if version != self.loc_version:
            raise Exception('Версия не та')

    def switch_lang(self):
        self.find_element(ProductLocators.loc_lang_dropdown).click()
        self.find_element(ProductLocators.loc_lang_dropdown_nemu).click()
        time.sleep(0.1)

