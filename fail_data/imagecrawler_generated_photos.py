from bs4 import BeautifulSoup
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
from selenium.common.exceptions import NoSuchElementException
import ssl

# SSL 인증서 검증 비활성화
ssl._create_default_https_context = ssl._create_unverified_context

from IPython.core.display import display, HTML
display(HTML("<style>.output_area { max-height: none; }</style>"))

class ImageCrawler():
    def __init__(self):
        self.chrome_options = Options()
        self.chrome_options.add_experimental_option("detach", True)
        self.chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
        # self.chrome_options.add_argument('--headless') 
        self.executable_path = ChromeDriverManager().install()
        # self.service = Service(executable_path=ChromeDriverManager().install())
        self.browser = None

    def __enter__(self):
        self.browser = webdriver.Chrome(executable_path=self.executable_path, options=self.chrome_options)
        # self.browser = webdriver.Chrome(service=self.service, options=self.chrome_options)
        self.browser.maximize_window()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.browser.quit()

    def download_images(self):
        url = "https://generated.photos/faces/front-facing/young-adult/asian-race/brown-eyes"
        self.browser.get(url)
        self.browser.implicitly_wait(5)

        #-------------- 여기서부터

        SCROLL_PAUSE_TIME = 2

        load_more_button = self.browser.find_element(By.CSS_SELECTOR, ".loadmore-btn")
        load_more_count = 0
        try:    
            while load_more_button.is_displayed():
                self.browser.execute_script("arguments[0].scrollIntoView();", load_more_button)
                time.sleep(2)
                last_height = self.browser.execute_script('return document.body.scrollHeight')
                while True:
                    self.browser.execute_script('window.scrollTo(0, document.body.scrollHeight);')
                    time.sleep(SCROLL_PAUSE_TIME)
                    new_height = self.browser.execute_script('return document.body.scrollHeight')
                    if new_height == last_height:
                        break
                    last_height = new_height
                load_more_button.click()
                time.sleep(2)
                load_more_button = self.browser.find_element(By.CSS_SELECTOR, ".loadmore-btn")
                
                load_more_count += 1
                if load_more_count == 1100:
                    break
                
        except NoSuchElementException:
            pass
        #--------------- 여기까지는 스크롤 내리는 용도
        
        
        images = self.browser.find_elements(By.CSS_SELECTOR, "img[data-v-120d0d76]")
        count = 1
        for image in images:
            time.sleep(2)

            img_url = image.get_attribute('src')

            save_folder = 'C:/Users/jungh/final_project/img_path'
            
            save_path = os.path.join(save_folder, f'{count}.jpg')
            urllib.request.urlretrieve(img_url, save_path)
            count += 1

            if count == 25000:
                break
