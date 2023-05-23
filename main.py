from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
import time
from urllib.parse import quote
from selenium.webdriver.common.alert import Alert
import csv

with open('invalid.csv', 'a', newline='') as csv_file:
    writer = csv.writer(csv_file)


browser = webdriver.Chrome('C:/chromedriver/chromedriver')

browser.maximize_window()
# using this to login in whatsApp.
browser.get("https://web.whatsapp.com/")


search_xpath = '//div[@contenteditable="true"][@data-tab="3"]'

# this make sure you have enough time to Scan Qr Code and login.
search_box = WebDriverWait(browser, 5000).until(
    EC.presence_of_element_located((By.XPATH, search_xpath))
)


message = ''' message message message message message message message message message message message message message message message 
'''

with open("numbers.csv", 'r', encoding="utf-8-sig") as file:
    csvreader = csv.reader(file)
    for row in csvreader:
        phnNo = ''.join(filter(str.isdigit, row))
        phnNo = "91" + str(phnNo)
        phnNo = int(phnNo)
        browser.get(
            f"https://web.whatsapp.com/send?phone={phnNo}&text={quote(message)}")

        try:
            Alert(browser).accept()
        except:
            print("No Alert")

        page_load = WebDriverWait(browser, 50).until(
            EC.presence_of_element_located((By.TAG_NAME, "body"))
        )

        try:
            valid_box = WebDriverWait(browser, 5).until(
                EC.presence_of_element_located(
                    (By.XPATH, "//div[text()='Phone number shared via url is invalid.']"))
            )
            valid_box_button = browser.find_element(By.XPATH,"//button[@data-testid='popup-controls-ok']")
            valid_box_button.click()
            print("invalid No " + str(phnNo))
            with open('invalid.csv', 'a', newline='') as csv_file:
                writer = csv.writer(csv_file)
                new_row = [str(phnNo)]
                writer.writerow(new_row)
            continue
        except TimeoutException:
            print("Valid Number " + str(phnNo))

        input_xpath = '//div[@contenteditable="true"][@data-tab="10"]'

        try:
            input_box = WebDriverWait(browser, 50).until(
                EC.presence_of_element_located((By.XPATH, input_xpath))
            )
        except TimeoutException:
            print("page is taking time to load")
            with open('tryagain.csv', 'a', newline='') as csv_file:
                wri = csv.writer(csv_file)
                new_row = [str(phnNo)]
                wri.writerow(new_row)
            continue

        input_box = browser.find_element(By.XPATH, input_xpath)
        input_box.send_keys(Keys.ENTER)

        time.sleep(1)

time.sleep(15)
