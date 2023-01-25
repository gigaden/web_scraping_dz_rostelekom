from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium_stealth import stealth
from bs4 import BeautifulSoup

import time

from crud import insert_from_citilink
from settings import TOTAL_PAGE_CITILINK, TIME_SLEEP_CITILINK

options = webdriver.ChromeOptions()
options.add_argument("start-maximized")

options.add_experimental_option("excludeSwitches", ["enable-automation"])
options.add_experimental_option('useAutomationExtension', False)
options.add_argument("--disable-blink-features=AutomationControlled")

driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

stealth(driver,
        languages=["en-US", "en"],
        vendor="Google Inc.",
        platform="Win64",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
        )


# запускаем наш парсинг. Ситилинк может выдать два варианта при обращении к странице
# классы для поиска в каждом варианте свои
def scrap_citilink():
    for page in range(1, TOTAL_PAGE_CITILINK + 1):
        start_url = f'https://www.citilink.ru/catalog/noutbuki/?p={page}&f=available.all&view_type=list'
        driver.get(start_url)
        time.sleep(TIME_SLEEP_CITILINK)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        # первый вариант
        if 'class' in soup.html.attrs:
            cards = soup.find_all('div',
                                  'product_data__gtm-js product_data__pageevents-js ProductCardHorizontal js--ProductCardInListing js--ProductCardInWishlist')
            for card in cards:
                price = int((card.find('span',
                                       'ProductCardHorizontal__price_current-price js--ProductCardHorizontal__price_current-price').get_text()).replace(
                    ' ', ''))
                href = 'https://www.citilink.ru' + card.find('a',
                                                             'ProductCardHorizontal__title Link js--Link Link_type_default').get(
                    'href')
                title = card.find('a', 'ProductCardHorizontal__title Link js--Link Link_type_default').get('title')
                insert_from_citilink(price, href, title)
            print(f'Page {page} from Citilink done. Go next page...')
        # второй вариант
        else:
            cards = soup.find_all('div', 'app-catalog-rjg8ao e1btxpey0')
            for card in cards:
                price = int(card.find('span', 'app-catalog-0 eb8dq160').get('data-meta-price'))
                href = 'https://www.citilink.ru' + card.find('a', 'app-catalog-9gnskf e1259i3g0').get('href')
                title = card.find('a', 'app-catalog-9gnskf e1259i3g0').get('title')
                insert_from_citilink(price, href, title)
            print(f'Page {page} from Citilink done. Go next page...')
    driver.close()
