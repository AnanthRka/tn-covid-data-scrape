from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import os 
import time

option = webdriver.ChromeOptions()
# option.add_argument('--headless')
option.add_argument("--log-level=3")
option.add_argument("window-size=1200x600")
option.add_experimental_option('excludeSwitches', ['enable-logging'])
prefs = {'download.default_directory': 'S:\Ananth\dataset'}
option.add_experimental_option('prefs', prefs)

os.environ['WDM_LOG_LEVEL'] = '0'
driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
driver.maximize_window()
driver.set_page_load_timeout(10)
# alternate_url = 'https://tn.data.gov.in/keywords/covid-19-tamil-nadu'
url = 'https://tn.data.gov.in/search/site?filter%5Bnew_title%5D=covid+districtwise+statistics+all+cases&page=1'
page = 1
document = 1
filename = 'S:\Ananth\dataset\districtwise_statistics_of_covid_19_cases_in_tn_as_on_18_08_2021'

while True:
    print(f'Going to page {page}')
    try:
        driver.get(url)
    except TimeoutException:
        driver.get('htpps://google.com')
        time.sleep(1)
        driver.get(url)

    h3 = driver.find_elements_by_tag_name('h3')
    urls = [i.find_element_by_tag_name('a').get_attribute('href') for i in h3]
    
    try:
        url = driver.find_element_by_link_text('Next').get_attribute('href')
    except NoSuchElementException:
        next = None

    for i in urls:
        try:
            print(f'Getting file in {i}')
            driver.get(i)
            if document%5 ==0:
                driver.implicitly_wait(5)
        except TimeoutException:
            driver.get(i)
            driver.implicitly_wait(10)
        time.sleep(1)

        date = driver.find_element_by_class_name('title-content').text
        date = date[len(date)-10:]
        date = date.replace('/', '_')
        filename = filename[:len(filename)-10] + date + '.csv'
        driver.find_element_by_xpath('//*[@id="web_catalog_tab_block_10"]/div/div/div/div[2]/div/a').click()
        time.sleep(1)
        driver.find_element_by_xpath('//*[@id="edit-download-reasons"]/div[2]/label').click()
        driver.find_element_by_xpath('//*[@id="edit-reasons-d"]/div[1]/label').click()
        # time.sleep(1)
        driver.find_element_by_xpath('//*[@id="edit-mail-d"]').send_keys(Keys.ENTER)
        time.sleep(3)

        if not os.path.exists(filename):
            time.sleep(2)
        p = driver.window_handles[0]
        child = driver.window_handles[1]
        driver.switch_to.window(child)
        driver.close()
        driver.switch_to.window(p)
        print(f'Downloaded {document} documents')
        document +=1

    page +=1
    print()
    if next is None:
        break

driver.quit()