from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
import pandas as pd
import time
import random

# URL 설정
DISNEY_PLUS_URL = "https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?release_year_from=2024&release_year_until=2024&rating_imdb=6&tomatoMeter=60"

# 작품 정보 저장 리스트
titles = []
genres = []
ratings_IMDB = []
ratings_TOMATO = []
age_ratings = []
production_countries = []
detail_urls = []


# ChromeDriver 설정
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.get(DISNEY_PLUS_URL)
time.sleep(5)  # 페이지 로드 대기

# 무한 스크롤링을 통해 모든 작품의 상세 페이지 URL 수집
def scroll_and_collect_urls():
    last_height = driver.execute_script("return document.body.scrollHeight")
    
    while True:
        # 현재 페이지 데이터 크롤링
        items = driver.find_elements(By.CSS_SELECTOR, 'div[data-testid="titleItem"] a')
        for item in items:
            detail_url = item.get_attribute('href')
            if detail_url not in detail_urls:
                detail_urls.append(detail_url)
        
        # 페이지 끝까지 스크롤
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        
        # 새로운 콘텐츠 로드 대기
        time.sleep(2)
        
        # 새로운 스크롤 높이 계산
        new_height = driver.execute_script("return document.body.scrollHeight")
        
        # 새로운 콘텐츠가 로드되지 않았으면 종료
        if new_height == last_height:
            break
        
        last_height = new_height

# 상세 페이지에서 데이터 크롤링
def collect_data_from_detail_pages():
    for url in detail_urls:
        driver.get(url)  # 상세 페이지로 이동
        time.sleep(3)  # 페이지 로드 대기
        
        try:
            # 제목 크롤링
            title = driver.find_element(By.CLASS_NAME, "title-detail-hero__details__title").text.strip()
            
            # 장르 크롤링
            genre_elements = driver.find_elements(By.CSS_SELECTOR, "#base > div:nth-child(2) > div.title-detail.new-buy-box > div > div.title-sidebar.title-detail__sidebar > aside > div > div.title-info.title-info > div:nth-child(2) > div > span")
            genres_combined = [g.text.strip() for g in genre_elements]
            genre = ", ".join(genres_combined) if genres_combined else "Unknown Genre"
            
            # 평점 크롤링
            # IMDB 값 추출
            try:
                imdb_xpath = "//div[contains(@class, 'jw-scoring-listing__rating--group') and .//img[@alt='IMDB']]/div"
                imdb_element = driver.find_element(By.XPATH, imdb_xpath)
                imdb_text = imdb_element.text.strip()
                print("IMDB Score:", imdb_text)

            except:
                imdb_text = "전문가 평점이 없음"

            # ROTTEN TOMATOES 값 추출
            try:
                rt_xpath = "//div[contains(@class, 'jw-scoring-listing__rating--group') and .//img[@alt='ROTTEN TOMATOES']]/span"
                rt_element = driver.find_element(By.XPATH, rt_xpath)
                rt_score = rt_element.text.strip()
                print("ROTTEN TOMATOES Score:", rt_score)  # 79%
            except:
                rt_score = "전문가 평점이 없음"
            
            # 연령 등급 크롤링
            try: 
                xpath = "//h3[contains(text(), '연령 등급')]/following-sibling::div"
                element = driver.find_element(By.XPATH, xpath)
                age = element.text
            except:
                age = "전체 이용가"
                
            # 첫 번째 : 한국
            # 두 번째 : 미국, 중국
            # 세 번째 : 영국, 이탈리아
            # 제작 국가 크롤링
            try:
                xpath = "//h3[contains(text(), '제작 국가')]/following-sibling::div"
                element = driver.find_element(By.XPATH, xpath)
                production_country = element.text
            except:
                production_country = "Unknown Production Country"
            

            
            # 데이터 저장
            titles.append(title)
            genres.append(genre)
            age_ratings.append(age)
            production_countries.append(production_country)
            ratings_IMDB.append(imdb_text)
            ratings_TOMATO.append(rt_score)
            # list : append
            
            
            
            print(f"Collected: {title} | {genre} | {age} | {production_country}, {imdb_text}, {rt_score}")
        except Exception as e:
            print(f"Error processing URL {url}: {e}")

# 메인 페이지에서 모든 작품의 상세 페이지 URL 수집
scroll_and_collect_urls()

# 각 상세 페이지에서 데이터 크롤링
collect_data_from_detail_pages()

# 데이터 저장
data = {
    "Title": titles,
    "Genre": genres,
    "Rating IMDB": ratings_IMDB,
    "Rating TOMATO": ratings_TOMATO,
    "Age Rating": age_ratings,
    "Production Country": production_countries,
    "OTT": "Netplix"
}
df = pd.DataFrame(data)
df.to_csv("Netflix_00.csv", index=False, encoding="utf-8-sig")

print(f"총 {len(df)}개의 작품 정보를 크롤링했습니다.")