import requests
from bs4 import BeautifulSoup

# 크롤링할 URL
url = "https://www.justwatch.com/kr/%EB%8F%99%EC%98%81%EC%83%81%EC%84%9C%EB%B9%84%EC%8A%A4/netflix?release_year_from=2024&release_year_until=2024&rating_imdb=6&tomatoMeter=60"
# 요청 헤더 설정
headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"
}

# 웹 페이지 요청
response = requests.get(url, headers=headers)

if response.status_code == 200:
    # 페이지 파싱
    soup = BeautifulSoup(response.text, 'html.parser')
    
    # 원하는 데이터 추출 (예: data-title 속성)
    titles = soup.find_all('div', {'data-testid': 'titleItem'})
    for title in titles:
        data_title = title.get('data-title')
        if data_title:
            print(data_title)
else:
    print(f"Failed to retrieve the webpage. Status code: {response.status_code}")
