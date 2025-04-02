# 인천국제공항 실시간 정보 시스템

인천국제공항의 실시간 입국장 혼잡도 및 항공편 정보를 제공하는 스트림릿 애플리케이션입니다. 공공데이터포털 API를 활용하여 개발되었습니다.

## 주요 기능

- 실시간 입국장 혼잡도 모니터링
- 항공편 검색 및 정보 조회
- 터미널별 입국장 및 항공사 카운터 정보 제공
- 공항 교통 정보 안내

## 설치 방법

```bash
# 레포지토리 복제
git clone https://github.com/youni202/incheon-airport-info-app.git
cd incheon-airport-info-app

# 필요한 라이브러리 설치
pip install -r requirements.txt

# 앱 실행
streamlit run app.py
```

## 데이터 출처

- 인천국제공항공사 공공데이터 API (공공데이터포털)
- API 엔드포인트: http://apis.data.go.kr/B551177/StatusOfArrivals/getArrivalsCongestion

## 라이선스

MIT License