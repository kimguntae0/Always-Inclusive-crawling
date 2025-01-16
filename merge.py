import pandas as pd

# 파일 경로 설정
netflix_file_path = r'C:\Users\kmg63\OneDrive\바탕 화면\Final_project\Netflix_cleaned.csv'
disney_file_path = r'C:\Users\kmg63\OneDrive\바탕 화면\Final_project\disney_plus_details_cleaned.csv'
output_file_path = r'C:\Users\kmg63\OneDrive\바탕 화면\Final_project\Merged_details.csv'

# CSV 파일 로드
netflix_df = pd.read_csv(netflix_file_path)
disney_df = pd.read_csv(disney_file_path)

# 데이터프레임 병합 (Title 열을 기준으로)
merged_df = pd.concat([netflix_df, disney_df], ignore_index=True)

# 병합된 데이터프레임 저장
merged_df.to_csv(output_file_path, index=False, encoding='utf-8-sig')

print("데이터 병합 완료")