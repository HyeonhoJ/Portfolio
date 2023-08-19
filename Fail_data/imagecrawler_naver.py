from bs4 import     
import selenium
from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import urllib.request
import os
import shutil


class ImageCrawler():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        self.chrome_options.add_argument('--headless') 
        self.service = Service(executable_path=ChromeDriverManager().install())
        self.browser = None

    def __enter__(self):
        self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.browser.maximize_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def download_images(self, celebrity, folder_name):
        keword_input = celebrity.replace(' ', '+')

        url = f"https://search.naver.com/search.naver?where=image&query={keword_input}"
        self.browser.get(url)
        self.browser.implicitly_wait(5)

        images = self.browser.find_elements(By.CSS_SELECTOR, "._image._listImage")

        count = 1
        for image in images:
            image.click()
            time.sleep(3)

            img_url = image.get_attribute('src')

            save_folder = f'C:/Users/jungh/final_project/img_path/{folder_name}/'
            os.makedirs(save_folder, exist_ok=True)
            save_path = os.path.join(save_folder, f'{count}.jpg')
            urllib.request.urlretrieve(img_url, save_path)
            count += 1

            if count == 41:
                break
