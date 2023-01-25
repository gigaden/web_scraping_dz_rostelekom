from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from webdriver_manager.chrome import ChromeDriverManager

from selenium_stealth import stealth
from bs4 import BeautifulSoup

import time

from crud import insert_from_dns
from settings import TOTAL_PAGE_DNS, TIME_SLEEP_DNS

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


# запускаем наш парсинг DNS
def scrap_dns():
    for page in range(1, TOTAL_PAGE_DNS + 1):
        start_url = f'https://www.dns-shop.ru/catalog/17a892f816404e77/noutbuki/?stock=now&p={page}&mode=simple'
        driver.get(start_url)
        time.sleep(TIME_SLEEP_DNS)
        soup = BeautifulSoup(driver.page_source, 'lxml')

        cards = soup.find_all('div', 'catalog-product ui-button-widget')
        for card in cards:
            price = card.find('div', 'product-buy__price').get_text()
            href = 'https://www.dns-shop.ru' + card.find('a', 'catalog-product__name ui-link ui-link_black').get('href')
            title = card.find('a', 'catalog-product__name ui-link ui-link_black').span.get_text()
            insert_from_dns(price, href, title)
        print(f'Page {page} from Dns done. Go next page...')
