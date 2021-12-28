from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from pymongo import MongoClient
from pprint import pprint
from pymongo.errors import DuplicateKeyError as dke

chrome_options = Options()
chrome_options.add_argument('start-maximized')
driver = webdriver.Chrome(options=chrome_options)

driver.get('https://www.mvideo.ru/')

client = MongoClient('127.0.0.1', 27017)
db = client['m_video_ru']
goods = db.goods

driver.execute_script("window.scrollTo(0, 1700)")

wait = WebDriverWait(driver, 10)
button = wait.until(EC.element_to_be_clickable((By.XPATH,
                                                "//span[contains(text(),'В "
                                                "тренде')]")))
button.click()

box_blocks = driver.find_element(By.TAG_NAME, 'mvid-shelf-group')
items_names = box_blocks.find_elements(By.XPATH,
                                       ".//div[contains(@class, "
                                       "'product-mini-card__name')]")
items_prices = box_blocks.find_elements(By.XPATH,
                                        ".//div[contains(@class, "
                                        "'product-mini-card__price')]")
items_discount = box_blocks.find_elements(By.XPATH,
                                          ".//div[contains(@class,'value')]")

goods_list = []
for n_el in range(len(items_names)):
    good_list = {'Наименование': items_names[n_el].text,
                 'Цена': items_prices[n_el].text.replace(' ', '').split()[0],
                 'Скидка': items_discount[n_el].text}
    goods_list.append(good_list)

    try:
        goods.insert_one(good_list)
    except dke:
        pass

pprint(goods_list)

driver.close()
