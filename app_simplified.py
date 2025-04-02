import streamlit as st
import pandas as pd
import requests
import time
from datetime import datetime

# 페이지 설정
st.set_page_config(
    page_title="인천국제공항 실시간 정보",
    page_icon="✈️",
    layout="wide"
)

# API 키 설정
API_KEY = "4q1sVXi0cPESZlljpKfTU7CxdXYfGycZKuBakPEOYWMHS4h8VaetyuTMI89MS12gmh2jd1uiBrkEzKc%2FzqVg4w%3D%3D"
BASE_URL = "http://apis.data.go.kr/B551177/StatusOfArrivals/getArrivalsCongestion"

# 헤더
st.title("✈️ 인천국제공항 입국장 정보")
st.markdown("실시간 입국장 혼잡도 및 항공편 정보를 확인할 수 있습니다.")

# 사이드바
st.sidebar.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Incheon_International_Airport_logo.svg/320px-Incheon_International_Airport_logo.svg.png", width=200)
st.sidebar.title("검색 옵션")

# 터미널 선택
terminal = st.sidebar.selectbox(
    "터미널 선택:",
    options=["T1", "T2"],
    index=0
)

# 공항 코드 입력
airport_code = st.sidebar.text_input("출발지 공항 코드 (예: HKG)")

# 데이터 가져오기
def fetch_data(terminal, airport=None):
    params = {
        "serviceKey": API_KEY,
        "numOfRows": 100,
        "pageNo": 1,
        "terno": terminal,
        "type": "json"
    }
    
    if airport:
        params["airport"] = airport
    
    try:
        response = requests.get(BASE_URL, params=params)
        data = response.json()
        
        if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
            items = data['response']['body']['items']
            if isinstance(items, dict) and 'item' in items:
                if isinstance(items['item'], list):
                    return pd.DataFrame(items['item'])
                else:
                    return pd.DataFrame([items['item']])
        
        return pd.DataFrame()
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

# 데이터 전처리
def preprocess_data(df):
    if df.empty:
        return df
    
    # 데이터 타입 변환
    if 'foreigner' in df.columns:
        df['foreigner'] = pd.to_numeric(df['foreigner'], errors='coerce').fillna(0)
    if 'korean' in df.columns:
        df['korean'] = pd.to_numeric(df['korean'], errors='coerce').fillna(0)
    
    # 날짜 변환
    if 'estimatedtime' in df.columns:
        df['estimatedtime'] = pd.to_datetime(df['estimatedtime'], format='%Y%m%d%H%M', errors='coerce')
    if 'scheduletime' in df.columns:
        df['scheduletime'] = pd.to_datetime(df['scheduletime'], format='%Y%m%d%H%M', errors='coerce')
    
    return df

# 검색 버튼
if st.sidebar.button("정보 조회", use_container_width=True):
    with st.spinner("데이터를 불러오는 중..."):
        df = fetch_data(terminal, airport_code if airport_code else None)
        df = preprocess_data(df)
    
    if not df.empty:
        # 탭 생성
        tab1, tab2 = st.tabs(["📊 혼잡도 현황", "✈️ 항공편 정보"])
        
        # 탭 1: 혼잡도 현황
        with tab1:
            st.subheader("입국장 혼잡도")
            
            # 요약 정보
            if 'korean' in df.columns and 'foreigner' in df.columns:
                total_korean = df['korean'].sum()
                total_foreigner = df['foreigner'].sum()
                total_people = total_korean + total_foreigner
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("총 대기 인원", f"{int(total_people)}명")
                
                with col2:
                    st.metric("내국인", f"{int(total_korean)}명")
                
                with col3:
                    st.metric("외국인", f"{int(total_foreigner)}명")
            
            # 입국장별 혼잡도
            if 'entrygate' in df.columns:
                st.subheader("입국장별 대기 인원")
                
                # 입국장별 통계
                gate_summary = df.groupby('entrygate').agg({
                    'korean': 'sum',
                    'foreigner': 'sum'
                }).reset_index()
                
                gate_summary['total'] = gate_summary['korean'] + gate_summary['foreigner']
                
                # 입국장별 대기 인원 차트
                st.bar_chart(gate_summary.set_index('entrygate')[['korean', 'foreigner']])
        
        # 탭 2: 항공편 정보
        with tab2:
            st.subheader("항공편 정보")
            
            # 항공편 검색
            search_col1, search_col2 = st.columns(2)
            
            with search_col1:
                search_flight = st.text_input("편명 검색 (예: KE123)")
            
            with search_col2:
                search_airport = st.text_input("출발지 공항 검색 (예: HKG)")
            
            # 검색 버튼
            search_btn = st.button("검색")
            
            if search_btn or search_flight or search_airport:
                search_results = df.copy()
                
                if search_flight:
                    search_results = search_results[search_results['flightid'].str.contains(search_flight, case=False, na=False)]
                
                if search_airport:
                    search_results = search_results[search_results['airport'].str.contains(search_airport, case=False, na=False)]
                
                if not search_results.empty:
                    st.success(f"{len(search_results)}개의 항공편이 검색되었습니다.")
                    
                    # 검색 결과 표시
                    columns = ['flightid', 'airport', 'entrygate', 'gatenumber', 'estimatedtime']
                    columns = [col for col in columns if col in search_results.columns]
                    
                    if columns:
                        result_df = search_results[columns].copy()
                        
                        # 컬럼명 변경
                        column_mapping = {
                            'flightid': '편명',
                            'airport': '출발지',
                            'entrygate': '입국장',
                            'gatenumber': '게이트',
                            'estimatedtime': '도착시간'
                        }
                        
                        result_df.rename(columns={col: column_mapping.get(col, col) for col in result_df.columns}, inplace=True)
                        
                        # 시간 형식 변경
                        if '도착시간' in result_df.columns:
                            result_df['도착시간'] = result_df['도착시간'].dt.strftime('%H:%M')
                        
                        st.dataframe(result_df)
                else:
                    st.warning("검색 결과가 없습니다.")
            
            # 모든 항공편 목록
            st.subheader("오늘의 도착 항공편")
            
            if not df.empty:
                display_columns = ['flightid', 'airport', 'entrygate', 'gatenumber', 'estimatedtime']
                display_columns = [col for col in display_columns if col in df.columns]
                
                if display_columns:
                    display_df = df[display_columns].copy()
                    
                    # 컬럼명 변경
                    column_mapping = {
                        'flightid': '편명',
                        'airport': '출발지',
                        'entrygate': '입국장',
                        'gatenumber': '게이트',
                        'estimatedtime': '도착시간'
                    }
                    
                    display_df.rename(columns={col: column_mapping.get(col, col) for col in display_df.columns}, inplace=True)
                    
                    # 시간 형식 변경
                    if '도착시간' in display_df.columns:
                        display_df['도착시간'] = display_df['도착시간'].dt.strftime('%H:%M')
                    
                    st.dataframe(display_df)
                else:
                    st.info("항공편 정보를 불러올 수 없습니다.")
            else:
                st.info("항공편 정보가 없습니다.")
    else:
        st.warning("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")

# 푸터
st.markdown("---")
st.markdown("© 2025 인천국제공항 정보 시스템 | 데이터 출처: 인천국제공항공사")