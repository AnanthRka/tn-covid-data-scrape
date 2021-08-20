from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException
import os

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
option.add_argument("--log-level=3")
option.add_experimental_option('excludeSwitches', ['enable-logging'])
prefs = {'download.default_directory': 'S:\Ananth\dataset'}
option.add_experimental_option('prefs', prefs)

os.environ['WDM_LOG_LEVEL'] = '0'
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)

driver.get('https://tn.data.gov.in/keywords/covid-19-tamil-nadu')
while True:
    h3 = driver.find_elements_by_tag_name('h3')
    urls =[]
    for i in h3:
        urls.append(i.find_element_by_tag_name('a').get_attribute('href'))

    for i in urls:
        print (i)
    print()
    try:
        driver.find_element_by_link_text('next ›').click()
    except NoSuchElementException:
        break

driver.quit()
