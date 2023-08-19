from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd
from bs4 import BeautifulSoup
import time

# 리뷰탭 긁어오는 함수
def save_contents(browser):
    try_cnt = 0
    wait = WebDriverWait(browser, 10)
    while True:
        try: 
            try_cnt+=1
            wait.until(
                EC.presence_of_element_located((By.CSS_SELECTOR, '#gdasContentsArea > div > div.review_list_wrap'))
                )
            content = browser.page_source.encode('utf-8').strip()
            soup = BeautifulSoup(content, 'html.parser')
            ul = soup.select_one('ul.inner_list')

            # id, 리뷰어 키워드, 상품 색상:
            color_names = [] # 데이터가 존재하지 않는 경우도 있음, None값이어서 getText()에러
            for i in  ul.select('li > div.review_cont'):
                try:
                    color_names.append(i.select_one('p.item_option').getText())
                except:
                    color_names.append(None)

            reviewers = [i.select_one('a.id').getText() for i in ul.select('li > div.info > div.user')]
            
            keywords = []
            for i in ul.select('li > div.info > div.user'):
                try:
                    keywords.append(i.select('p.tag > span'))
                except:
                    keywords.append(None)

            detail_scores = []
            for i in ul.select('li > div.review_cont'):
                try:
                    detail_score = []
                    for detail_bar in i.select('div.poll_sample > dl'):
                        detail_score.append([detail_bar.select_one('dt > span').getText(),detail_bar.select_one('dd > span.txt').getText()])
                    detail_scores.append(detail_score)
                except:
                    None
        

            # 평점, 날짜, 리뷰 내용
            scores = []
            for i in ul.select('li > div.review_cont > div.score_area > span.review_point'):
                try:
                    scores.append(i.select_one('span.point').getText())
                except:
                    scores.append(None)
            dates = []
            for i in ul.select('li > div.review_cont > div.score_area'):
                try:
                    dates.append(i.select_one('span.date').getText())
                except:
                    dates.append(None)
            reviews = []
            for i in ul.select('li > div.review_cont'):
                try:
                    reviews.append(i.select_one('div.txt_inner').getText())
                except:
                    reviews.append(None)
                    
            for i in range(len(reviewers)):
                row = {}
                row['product_id'] = product_id
                row['color_names'] = color_names[i]
                row['reviewers'] = reviewers[i]
                row['keywords'] = keywords[i]
                row['scores'] = scores[i]
                row['detail_score'] = detail_scores[i]
                row['review'] = reviews[i]
                row['date'] = dates[i]
                total_data.append(row)
            break
        except Exception as e:
            if try_cnt>=50:
                print("save contents error:", e)
                return True
            time.sleep(5)
            continue

def getUrl_and_clickReviewtab(url):
    while True:
        try:
            browser = webdriver.Chrome(service=service,options=chrome_options)
            wait = WebDriverWait(browser, 10)
            browser.get(url)

            #리뷰탭 클릭
            wait.until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, '#reviewInfo > a'))
                )
            review_tab = browser.find_element(By.CSS_SELECTOR, "#reviewInfo > a") # 찾기 
            review_tab.click()
            return browser
        except Exception as e:
            time.sleep(5)
            continue

chrome_options = Options()
chrome_options.add_experimental_option("detach", True)
chrome_options.add_experimental_option("excludeSwitches", ["enable-logging"])
service=Service(executable_path='./chromedriver.exe')

csv_path = '' # 파일 저장 경로 입력
total_data = []
prd_id_name = []

# 블러셔, 립, 섀도우
urls = ["https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000200010006&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat1000001000200010006_Small",
        "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=100000100020006&fltDispCatNo=&prdSort=01&pageIdx=2&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=0&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat100000100020006_Small&amplitudePageGubun=&t_page=&t_click=&midCategory=%EB%A6%BD%EB%A9%94%EC%9D%B4%ED%81%AC%EC%97%85&smallCategory=%EC%A0%84%EC%B2%B4&checkBrnds=&lastChkBrnd=",
        "https://www.oliveyoung.co.kr/store/display/getMCategoryList.do?dispCatNo=1000001000200070003&fltDispCatNo=&prdSort=01&pageIdx=1&rowsPerPage=24&searchTypeSort=btn_thumb&plusButtonFlag=N&isLoginCnt=1&aShowCnt=0&bShowCnt=0&cShowCnt=0&trackingCd=Cat1000001000200070003_Small&amplitudePageGubun=SMALL_CATE&t_page=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EA%B4%80&t_click=%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC%EC%83%81%EC%84%B8_%EC%86%8C%EC%B9%B4%ED%85%8C%EA%B3%A0%EB%A6%AC&midCategory=%EC%95%84%EC%9D%B4%EB%A9%94%EC%9D%B4%ED%81%AC%EC%97%85&smallCategory=%EC%86%8C_%EC%95%84%EC%9D%B4%EC%84%80%EB%8F%84%EC%9A%B0%2F%ED%8C%94%EB%A0%88%ED%8A%B8&checkBrnds=&lastChkBrnd=&t_3rd_category_type=%EC%86%8C_%EC%95%84%EC%9D%B4%EC%84%80%EB%8F%84%EC%9A%B0%2F%ED%8C%94%EB%A0%88%ED%8A%B8"
        ]


for i, url in enumerate(urls):
    browser = webdriver.Chrome(service=service,options=chrome_options)
    wait = WebDriverWait(browser, 15)
    browser.get(url)
    wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#Contents')))

    if i==0:
        selector = f'#Contents > ul.cate_list_box > li:nth-child(3) > a'
    elif i==1:
        selector = f'#Contents > ul.cate_list_box > li:nth-child(1) > a'
    else:
        selector = f'#Contents > ul.cate_list_box > li:nth-child(5) > a'

    next_tab = browser.find_element(By.CSS_SELECTOR, selector)
    next_tab.click()

    page_num=1
    while True:  
        try:
            if page_num ==1:
                page = 'strong'
            else:
                page = "a:nth-child(%d)"%page_num
            # page_num+=1
            
            next_num = browser.find_element(By.CSS_SELECTOR, '#Container > div.pageing >'+page)
            next_num.click()
            # wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, '#Container > div.pageing >'+page)))

            soup = BeautifulSoup(browser.page_source,'html.parser')
            prd_info = soup.select('div.prd_name')
            links = [a.find('a', class_=['goodsList']) for a in prd_info]
            for link in links:
                product_id = link['data-ref-goodsno']
                product_name = link['data-attr'].split('^')[-2]
                prd_id_name.append([product_id, product_name])
            
            page_num += 1

        except Exception:
            try:
                next_num = browser.find_element(By.CSS_SELECTOR, '#Container > div.pageing > a.next')
                next_num.click()
            except:
                break

    browser.quit()

last_point = None
# 제품 링크의 product_id로 링크에 접근
new_product_ids = prd_name_id.product_id.reset_index(drop=True).copy() 
while True:
    breaker = None
    # last point 부터 재시작
    if last_point != None:
        new_product_ids = new_product_ids[last_point:].reset_index(drop=True).copy()
        last_point = None
        review_data = pd.DataFrame(total_data)
        review_data.to_csv("%s.csv"%csv_path)

    for j, product_id in enumerate(new_product_ids):
        url = "https://www.oliveyoung.co.kr/store/goods/getGoodsDetail.do?goodsNo=" + product_id
        browser = getUrl_and_clickReviewtab(url)
        wait = WebDriverWait(browser, 10)    
        
        # 제품 정보 크롤링
        # title, price
        title = soup.select_one('#Contents > div.prd_detail_box.renew > div.right_area > div > p.prd_name').getText()
        brand = soup.select_one("#moveBrandShop").getText()
        price = soup.select_one('#Contents > div.prd_detail_box.renew > div.right_area > div > div.price > span.price-2 > strong').getText()
        score = soup.select_one("#repReview > b").getText()
        total = soup.select_one("#repReview > em").getText() 
        prd_id = product_id

        # 컬러 상세 이미지 가져오기
        colors = browser.find_elements(By.CSS_SELECTOR, '.thumb-color')
    
        if len(colors) >= 1
            for color in range(len(colors)):
                if color == 12:
                        wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, 'button.btn_more_colorchip'))
                        )
                        browser.find_element(By.CSS_SELECTOR, 'button.btn_more_colorchip').click()
                wait.until(
                        EC.element_to_be_clickable((By.CSS_SELECTOR, f'#colrParet_{color}'))
                        )
                browser.find_element(By.CSS_SELECTOR, f'#colrParet_{color}').click()
                
                soup = BeautifulSoup(browser.page_source,'html.parser')
                main_img = soup.select_one("#mainImg")['src']
                color_img = soup.select_one(f'#colrParet_{color} > span > img')['src']
                img_name = soup.select_one('#goodstxt').getText()

                product_data_data.append([title, price, color_img, main_img, img_name, brand, score, total, prd_id])

        else:

            main_img = soup.select_one("#mainImg")['src']
            color_img = soup.select_one("#mainImg")['src']
            img_name = title
            shadow_data.append([title, price, color_img, main_img, img_name, brand, score, total, prd_id])

        # 리뷰 데이터 크롤링
        page_num = 1
        try_cnt = 0
        while True:
            try_cnt+=1
            try:
                review_cnt = int(browser.find_element(By.CSS_SELECTOR, "#reviewInfo > a > span").text.replace('(','').replace(')','').replace(',',''))
                break
            except:
                if try_cnt >= 30:
                    print("리뷰 수")
                    browser.quit()
                    browser = getUrl_and_clickReviewtab(url)
                    wait = WebDriverWait(browser, 10)
                continue

        if review_cnt==0:
            browser.quit()
            continue

        page_end=False # 완료 확인        
        while True:
            time.sleep(1)

            # 페이지 모두 크롤링 완료
            if page_end==True:
                review_data = pd.DataFrame(total_data)
                review_data.to_csv("%s.csv"%csv_path)
                browser.quit()
                break
                    
            try_cnt = 0
            while True:
                try:
                    try_cnt+=1
                    wait.until(
                    EC.presence_of_element_located((By.CSS_SELECTOR, '#gdasContentsArea > div > div.pageing'))
                    )           
                    page_len = len(browser.find_elements(By.CSS_SELECTOR, '#gdasContentsArea > div > div.pageing > a'))+1 # 각 페이지 당 클릭 가능한 페이지 수 + 현재 페이지
                    page_bar = browser.find_element(By.CSS_SELECTOR, '#gdasContentsArea > div > div.pageing') # 페이지 바
                    break
                except Exception as e:
                    if try_cnt >= 30:
                        last_point = j
                        breaker = True
                        error = "페이지 바"
                        break
                    time.sleep(5)
                    continue

            if breaker == True:
                break

            next_page = 'a:nth-child(%d)'%page_num # 페이지 태그
            while True:
                try:
                    try:
                        page = page_bar.find_element(By.CSS_SELECTOR, next_page)
                    except:
                        page = page_bar.find_element(By.CSS_SELECTOR, 'strong')
                    break
                except:
                    if try_cnt>=30:
                        last_point = j
                        breaker = True
                        error = "페이지 바 요소"
                        break
                    continue
            
            if breaker == True:
                break
            
            page_label = page.text
            while True:
                try:
                    # 클릭할 페이지가 페이지 바 길이보다 길면 end
                    if page_num > page_len:
                        page_end = True
                    elif page_label == '이전 10 페이지':
                        page_num+=1
                    elif page_label == '다음 10 페이지':
                        page.click()
                        page_num=1
                    else:
                        page.click()
                        retry = save_contents(browser)
                        page_num+=1
                    if retry == True:
                        last_point = j
                        breaker = True
                        error = "페이징"
                    break
                except Exception as e:         


                    time.sleep(5)
                    continue

            if breaker == True:
                break
        if breaker == True:
            break
    if breaker == True:
        break

