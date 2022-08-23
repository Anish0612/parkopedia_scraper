import time
# from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
import pandas as pd
import os


def fetch(browser):
    WebDriverWait(browser, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, 'LocationDetailsTitleBar__title'))).click()

    # global title,spots,all_details,details,address,telepho
    try:
        title = browser.find_element(By.CLASS_NAME, 'LocationDetailsTitleBar__title').text
    except:
        title = None
    try:
        spots = browser.find_element(By.CLASS_NAME, 'LocationDetailsTitleBar__subTitle').text
    except:
        spots = None
    try:
        all_details = browser.find_element(By.CLASS_NAME, 'LocationDetailsContactDetails')
        details = all_details.find_elements(By.CLASS_NAME, 'LocationDetailsContactDetails__detail')
        address = None
        telephone_no = None
        website = None
        count = 0
        # address = location.text
        for one in details:
            if count == 0:
                address = one.text
                count += 1
            elif count == 1:
                telephone_no = one.text
                count += 1
            elif count == 2:
                website = one.text
                break
    except:
        address = None
        telephone_no = None
        website = None
    try:
        price = browser.find_element(By.CLASS_NAME, 'LocationDetailsPrices').text
    except:
        price = None
    try:
        WebDriverWait(browser, 50).until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'LocationDetailsTitleBar__closeButton'))).click()
    except:
        pass
    # close = browser.find_element(By.XPATH, '//*[@id="App"]/div/div/div/div[4]/div[1]/div[1]/div')
    # close_button.click()
    time.sleep(2)
    # print('Closing Data')
    # print('Complete Data')
    return title, spots, address, telephone_no, website, price


def open_website(name):
    options = webdriver.ChromeOptions()
    directory = os.getcwd()
    path = directory + '\\extension.crx'
    options.add_extension(path)
    time.sleep(5)
    browser = webdriver.Chrome(options=options)
    time.sleep(10)
    URL = 'https://www.parkopedia.com/'
    # URL = 'https://en.parkopedia.com/parking/carpark/bandra_kurla_complex_%E2%80%98g%E2%80%99_block_lot_4/400051/mumbai/?arriving=202207021530&leaving=202207021730'
    # name = 'Mumbai'
    browser.get(URL)
    window_name = browser.window_handles[0]
    browser.switch_to.window(window_name=window_name)
    all_result, browser = website_search(browser,name)
    return all_result, browser
    # break


def website_search(browser,name):
    while True:
        # search_link = WebDriverWait(browser,10).until(EC.visibility_of_element_located(By.XPATH,'//*[@id="searchContainer"]/div[3]/div/div/div[1]/form/div[1]/div/input'))
        search_link = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
            (By.XPATH, '//*[@id="searchContainer"]/div[3]/div/div/div[1]/form/div[1]/div/input')))
        # search_link = browser.find_element(By.XPATH,'//*[@id="searchContainer"]/div[3]/div/div/div[1]/form/div[1]/div/input')
        search_link.send_keys(name)
        time.sleep(5)
        search_link.send_keys(Keys.ENTER)
        time.sleep(2)
        try:
            # WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.XPATH, '//*[@id="searchContainer"]/div[3]/div/div/div[1]/form/div[2]/button'))).click()
            search_button = WebDriverWait(browser, 10).until(EC.visibility_of_element_located(
                (By.XPATH, '//*[@id="searchContainer"]/div[3]/div/div/div[1]/form/div[2]/button'))).click()
            # search_button.click()
            time.sleep(2)
            result = browser.find_element(By.CLASS_NAME, 'LocationsList')
            all_result = result.find_elements(By.CLASS_NAME, 'LocationListItem')
            return all_result, browser
        except:
            browser.get(URL)
            continue


URL = 'https://www.parkopedia.com/'
station = pd.read_excel('List of Stations for Parkopedia.xlsx')
# e
list_of_name = station['Station'].tolist()
# print(name)
for name in list_of_name:
    browser_close= False
    try:
        df1 = pd.read_excel('parkopedia.xlsx')
    except:
        df1 = pd.DataFrame()
    df = pd.DataFrame({'Place Name': [name],
                       'Spots': [None],
                       'Address': [None],
                       'Telephone No': [None],
                       'Website': [None],
                       'Price': [None]})
    df2 = pd.concat([df1, df])
    df2.to_excel('parkopedia.xlsx', index=False)
    try:
        all_result=website_search(browser,name)
    except:
        all_result, browser = open_website(name)
    while True:
        if len(all_result) == 0:
            break

        for single_result in all_result:
            try:
                single_result.click()
                title, spots, address, telephone_no, website, price = fetch(browser)
                browser_close = False
                # break
            except:
                browser.quit()
                browser_close = True
                print('Browser close')
                time.sleep(15)
                all_result, browser = open_website(name)
                if len(all_result) == 0:
                    browser_close = False
                # single_result.click()
                # title, spots, address, telephone_no, website, price = fetch(browser)
                print('2nd Try')
                break
            try:
                df1 = pd.read_excel('parkopedia.xlsx')
            except:
                df1 = pd.DataFrame()
            df = pd.DataFrame({'Place Name': [title],
                               'Spots': [spots],
                               'Address': [address],
                               'Telephone No': [telephone_no],
                               'Website': [website],
                               'Price': [price]})
            df2 = pd.concat([df1, df])
            df2.to_excel('parkopedia.xlsx', index=False)
            browser.execute_script("arguments[0].scrollIntoView();", single_result)
        # browser.execute_script("window.scrollTo(,document.body.scrollHeight)")
        if browser_close is True:
            continue
        else:
            break
        # print(result.text)
    time.sleep(2)
    browser.get(URL)
    # browser.get(URL)

    time.sleep(5)
    # print(all_price)
    # WebDriverWait(browser, 100).until(EC.visibility_of_element_located((By.XPATH, initial_XPATH))).click()

    # print(all_price.text)
    #
    # title, spots, address, telephone_no, website, price = fetch(browser)
    # print('Title', title)
    # print('spots', spots)
    # print('address', address)
    # print('telephone_no', telephone_no)
    # print('website', website)
    # print('price', price)

    # print(all_data)
    # browser.close()
    # # html = browser.page_source
    # #
    # # soup = BeautifulSoup(html,'lxml')
    # # print(soup)
browser.close()
browser.quit()
print('Completed')
