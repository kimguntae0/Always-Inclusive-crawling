import pandas as pd
from sklearn.preprocessing import MinMaxScaler

# 파일 경로 수정
file_path = r'C:\Users\kmg63\OneDrive\바탕 화면\Final_project\Netflix_00.csv'
output_path = r'C:\Users\kmg63\OneDrive\바탕 화면\Final_project\Netflix_cleaned.csv'

# 데이터 로드
df = pd.read_csv(file_path)

# 데이터 탐색
print(df.info())
print(df.describe())

# 결측치 처리
df['Genre'].fillna("Unknown Genre", inplace=True)
df['Rating IMDB'].fillna("No IMDB Rating", inplace=True)
df['Rating TOMATO'].fillna("No TOMATO Rating", inplace=True)
df['Age Rating'].fillna("No Age Rating", inplace=True)
df['Production Country'].fillna("Unknown Country", inplace=True)

# 중복 데이터 처리
df.drop_duplicates(inplace=True)  # 중복된 행 제거

# 불필요한 공백 제거
df['Title'] = df['Title'].str.strip()
df['Genre'] = df['Genre'].str.strip()
df['Age Rating'] = df['Age Rating'].str.strip()
df['Production Country'] = df['Production Country'].str.strip()

# 데이터 형식 변환
df['Rating IMDB'] = df['Rating IMDB'].str.extract(r'(\d+\.\d+)').astype(float)  # IMDB 평점 숫자 추출 및 변환
df['Rating TOMATO'] = df['Rating TOMATO'].str.rstrip('%').astype(float)  # TOMATO 평점 % 제거 및 변환

# 이상치 처리 (예: IMDB 평점이 0보다 작거나 10보다 큰 경우 제거)
df = df[(df['Rating IMDB'] >= 0) & (df['Rating IMDB'] <= 10)]

# 클린된 데이터 저장
df.to_csv(output_path, index=False, encoding='utf-8-sig')

print("데이터 클리닝 완료")