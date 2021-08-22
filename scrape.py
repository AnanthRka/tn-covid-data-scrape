from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.common.exceptions import NoSuchElementException, TimeoutException
from selenium.webdriver.common.keys import Keys
import os
import time
import glob


def driver_initialize():
    
    default_download_directory = os.getcwd() + r'\dataset'
    option = webdriver.ChromeOptions()
    # option.add_argument('--headless')
    option.add_argument("--log-level=3")
    option.add_argument("window-size=1200x600")
    option.add_experimental_option('excludeSwitches', ['enable-logging'])
    prefs = {'download.default_directory': default_download_directory}
    option.add_experimental_option('prefs', prefs)

    os.environ['WDM_LOG_LEVEL'] = '0'
    driver = webdriver.Chrome(ChromeDriverManager().install(), options=option)
    driver.maximize_window()
    driver.set_page_load_timeout(5)
    return driver

def download_file(driver, urls, documents, filename):
    
    for i in urls:  
        try:
            print(f'Getting file in {i}')
            driver.get(i)
            if documents%5 ==0:
                driver.implicitly_wait(5)
        except TimeoutException:
            driver.get(i)
            driver.implicitly_wait(10)
        time.sleep(1)

        date = driver.find_element_by_class_name('title-content').text
        date = date[len(date)-10:]
        date = date.replace('/', '_')
        filename = os.getcwd()+ r'\dataset\\' + filename[:len(filename)-10] + date + r'.csv'
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
        print(f'Downloaded {documents} documents')
        documents +=1
    return documents

def last_date_find():
    list_of_files = glob.glob(os.getcwd() +  r'\dataset\*.csv')
    if len(list_of_files)> 0:
        last_date_scraped = max(list_of_files, key=os.path.getctime)
        last_date_scraped = last_date_scraped[len(last_date_scraped)-14:len(last_date_scraped)-4].replace('_','/')
        documents = len(list_of_files) + 1
    else:
        last_date_scraped = ''
        documents = 1
    return last_date_scraped, documents

def main(pages=1, documents=1):

    try:
        # alternate_url = 'https://tn.data.gov.in/keywords/covid-19-tamil-nadu'
        next = f'https://tn.data.gov.in/search/site?filter%5Bnew_title%5D=covid+districtwise+statistics+all+cases&page={pages}'
        driver = driver_initialize()
        filename = 'districtwise_statistics_of_covid_19_cases_in_tn_as_on_18_08_2021'
        last_date_scraped= ''
        if os.path.exists( os.getcwd() + r'\dataset'):
            last_date_scraped, documents = last_date_find()
            print('Getting last updated filename...')

        if documents >1:
            needs_check = True
        else:
            needs_check = False
        
        while True:
            print(f'Going to page {pages}')
            try:
                driver.get(next)
            except TimeoutException:
                driver.get('htpps://google.com')
                time.sleep(1)
                driver.get(next)
                time.sleep(2)

            h3 = driver.find_elements_by_tag_name('h3')
            urls = [i.find_element_by_tag_name('a').get_attribute('href') for i in h3]

            if needs_check:
                print(f'Checking for the last date {last_date_scraped} in page {pages}')
                heads = [i.find_element_by_tag_name('a') for i in h3]
                for i in range(len(heads)):
                    if last_date_scraped in heads[i].text:
                        needs_check = False
                        urls = urls[i+1:]
                        break
                # documents += len(urls) -1
                        
                print('Already scraped this page')
                time.sleep(1)
            
            try:
                next = driver.find_element_by_link_text('Next').get_attribute('href')
            except NoSuchElementException:
                next = None
            
            if not needs_check:
                documents = download_file(driver, urls, documents, filename)
            pages +=1
            print()
            if next is None:
                break

    except Exception as e:
        print(e)
        driver.quit()
        print()
        main(pages,documents)


pages = 1
documents = 1
start_time =time.time()
main(pages,documents)
print(time.time() - start_time)