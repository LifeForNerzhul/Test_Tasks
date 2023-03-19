import pandas as pd
from selenium import webdriver
from bs4 import BeautifulSoup
import time


def clear_price(incorrect_price):
    if incorrect_price == "NoneType":
        return -1
    try:
        incorrect_price = incorrect_price.replace('\u2009', '')
    except TypeError:   # not every price has it, so just pass
        pass
    incorrect_price = int(incorrect_price[:incorrect_price.find('\xa0'):])
    return incorrect_price  # now it's correct)


dict_for_data = {
    'name': [],
    'price': [],
    'link': []
}
options = webdriver.FirefoxOptions()
# options.headless = True # браузер в фоне
browser = webdriver.Firefox(options=options)
browser.get('https://www.detmir.ru/catalog/index/name/strategic_games/')
time.sleep(5)
html = browser.page_source
soup = BeautifulSoup(html, 'html.parser')

# get number of goods
number_of_goods = soup.find('button', class_='eg xC ek ez eq eG eH').find('div', class_='ej').text
number_of_goods = number_of_goods[:number_of_goods.find(' '):]
number_of_goods = int(number_of_goods)

# count pages by - number of goods // goods per page(36)
number_of_page = number_of_goods // 36
if number_of_page != (number_of_goods / 36):
    number_of_page = number_of_page + 1

# find block with all goods and then all item in it
goods = soup.find('div', class_='gF')
goods = goods.findAll('section', class_='Iy IC yF')
for item in goods:
    dict_for_data['name'].append(item.find('h3', class_='IA').text)
    dict_for_data['link'].append(item.find('a', class_='II').get('href'))
    try:
        dict_for_data['price'].append(clear_price(item.find('span', class_='bgt bgu').text))
    except AttributeError:              # price without discount
        dict_for_data['price'].append(clear_price(item.find('span', class_='bgt').text))

#  working from the second page coz /page/0 or /page/1/ != first page
original_window = browser.current_window_handle
for page in range(2, number_of_page+1):
    browser.switch_to.new_window('tab')
    url = 'https://www.detmir.ru/catalog/index/name/strategic_games/page/' + str(page) + '/'
    browser.get(url)
    time.sleep(5)
    html = browser.page_source
    soup = BeautifulSoup(html, 'html.parser')

    goods = soup.find('div', class_='gF')
    goods = goods.findAll('section', class_='Iy IC yF')
    for item in goods:
        dict_for_data['name'].append(item.find('h3', class_='IA').text)
        dict_for_data['link'].append(item.find('a', class_='II').get('href'))
        try:
            dict_for_data['price'].append(clear_price(item.find('span', class_='bgt bgu').text))
        except AttributeError:          # price without discount
            try:
                dict_for_data['price'].append(clear_price(item.find('span', class_='bgt').text))
            except AttributeError:      # item without price - out of stock
                dict_for_data['price'].append(-1)
    browser.close()
    browser.switch_to.window(original_window)
pdTest = pd.DataFrame(dict_for_data)
pdTest.to_excel("output.xlsx")
browser.quit()