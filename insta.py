# login to instagram using selenium
#import getpass

#my_password = getpass.getpass("What is your password?\n")

#print(my_password)

from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.wait import WebDriverWait
from conf import MY_USERNAME, MY_PASSWORD
from selenium import webdriver
import time
from selenium.webdriver.support import ui
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import requests
import os
from urllib.parse import urlparse

PATH = "C:\Program Files (x86)\chromedriver.exe"
ser = Service(PATH)
op = webdriver.ChromeOptions()
browser = webdriver.Chrome(service=ser, options=op)

url = "https://www.instagram.com"
browser.get(url)

time.sleep(2)

username_el = browser.find_element(By.NAME, "username")
password_el = browser.find_element(By.NAME, "password")

username_el.send_keys(MY_USERNAME)
password_el.send_keys(MY_PASSWORD)

login_btn_el = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.CSS_SELECTOR, "button[type='submit']"))).click()

bt_now = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

bt_now2 = WebDriverWait(browser, 10).until(
    EC.element_to_be_clickable((By.XPATH, "//button[contains(text(), 'Not Now')]"))).click()

time.sleep(2)

the_rock_url = "https://www.instagram.com/therock/"
browser.get(the_rock_url)
post_xpath_str = "//a[contains(@href, '/p')]"
post_links = browser.find_elements_by_xpath(post_xpath_str)

post_link_el = None
if(len(post_links)>0):
   post_link_el = post_links[0]

if post_link_el != None:
    post_href = post_link_el.get_attribute('href')
    browser.get(post_href)


video_els = browser.find_elements_by_xpath("//video")
image_els = browser.find_elements_by_xpath("//img")

#make a directory for saving images
base_dir = os.path.dirname(os.path.abspath(__file__))
data_dir = os.path.join(base_dir, "data")
os.makedirs(data_dir, exist_ok=True)

def scrape_and_save(elements):
    for el in elements:
        #print(img.get_attribute('src'))
        url = el.get_attribute('src')
        base_url = urlparse(url).path
        filename = os.path.basename(base_url)
        filepath = os.path.join(data_dir, filename)
        
        if os.path.exists(filepath):
            continue
        with requests.get(url,stream=True) as r:
            try:
                r.raise_for_status()

            except:
                continue

            with open(filepath, 'wb') as f:
                for chunk in r.iter_content():
                    if chunk:
                        f.write(chunk)

#scrape_and_save(video_els)
#scrape_and_save(image_els)


"""
USE ML TO CLASSIFY THE POST'S IMAGE OR VIDEO AND THEN COMMENT IN A RELEVANT
"""

# method for automated comments
def auto_comment(content="That is cool"):
    comment_el_xpath = "//textarea[contains(@placeholder, 'Add a comment…')]"
    comment_el = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, comment_el_xpath)))
    comment_el.click()

    comment_el = WebDriverWait(browser, 10).until(EC.element_to_be_clickable((By.XPATH, comment_el_xpath)))
    comment_el.send_keys(content)

    time.sleep(5)
    post_btn_els = browser.find_elements(By.CSS_SELECTOR, "button[type='submit']")

    for btn in post_btn_els:
        try:
            btn.click()
        except:
            pass


# auto_comment()
def auto_like(browser):
    # the like button always has the greater height
    # we loop through all the like buttons and find the one with the largest height
    like_heart_svg_xpath = "//*[contains(@aria-label, 'Like')]"
    all_like_hearts_els = browser.find_elements(By.XPATH, like_heart_svg_xpath)
    max_heart_h = -1
    for heart_el in all_like_hearts_els:
        h = heart_el.get_attribute('height')
        current_h = int(h)

        if current_h > max_heart_h:
            max_heart_h = current_h

    like_heart_svg_xpath = "//*[contains(@aria-label, 'Like')]"
    all_like_hearts_els = browser.find_elements(By.XPATH, like_heart_svg_xpath)

    # get the height attribute and click on the one with the greatest height
    for heart_el in all_like_hearts_els:
        h = heart_el.get_attribute('height')
        if h == max_heart_h or h ==f"{max_heart_h}":
            parent_btn= heart_el.find_element(By.XPATH, "..") # goes up 1 level
            try:
                parent_btn.click()
            except:
                pass

auto_like(browser)
browser.find_element(By.TAG_NAME, '')