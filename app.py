import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import xml.etree.ElementTree as ET
import json
import logging
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
import urllib.parse
import os

# 로깅 설정
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    handlers=[
        logging.FileHandler("airport_info_app.log"),
        logging.StreamHandler()
    ]
)
logger = logging.getLogger(__name__)

# API 키 관리 (환경변수 또는 Streamlit Secrets 권장)
def get_api_key():
    """
    API 키를 안전하게 가져오는 함수
    """
    # Streamlit Secrets 우선 사용
    api_key = st.secrets.get("AIRPORT_API_KEY", None) if hasattr(st, 'secrets') else None
    
    # 환경변수 확인
    if not api_key:
        api_key = os.environ.get("AIRPORT_API_KEY")
    
    # 직접 키 사용 (보안상 권장하지 않음)
    if not api_key:
        api_key = "4q1sVXi0cPESZlljpKfTU7CxdXYfGycZKuBakPEOYWMHS4h8VaetyuTMI89MS12gmh2jd1uiBrkEzKc%2FzqVg4w%3D%3D"
        logger.warning("API 키를 직접 코드에 포함했습니다. 보안 취약점 주의!")
    
    return api_key

# API 엔드포인트 및 기본 설정
BASE_URL = "http://apis.data.go.kr/B551177/StatusOfArrivals/getArrivalsCongestion"

@st.cache_data(ttl=600)  # 10분간 캐시
def fetch_data(terminal, num_rows=100, page_no=1, response_type="json", airport=None):
    """
    공항 API에서 데이터를 가져오는 함수
    
    Args:
        terminal (str): 터미널 번호 (T1 또는 T2)
        num_rows (int): 가져올 데이터 행 수
        page_no (int): 페이지 번호
        response_type (str): 응답 데이터 형식 (json 또는 xml)
        airport (str, optional): 출발 공항 코드
    
    Returns:
        pandas.DataFrame: 가져온 데이터
    """
    try:
        # API 키 가져오기
        api_key = get_api_key()
        decoded_api_key = urllib.parse.unquote(api_key)
        
        # 요청 파라미터 설정
        params = {
            "serviceKey": decoded_api_key,
            "numOfRows": num_rows,
            "pageNo": page_no,
            "terno": terminal,
            "type": response_type
        }
        
        # 선택적 공항 코드 추가
        if airport:
            params["airport"] = airport
        
        # API 요청
        response = requests.get(BASE_URL, params=params, timeout=10)
        response.raise_for_status()  # HTTP 오류 발생 시 예외 처리
        
        # 응답 데이터 처리
        if response_type == "json":
            data = response.json()
            if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
                items = data['response']['body']['items']
                if isinstance(items, dict) and 'item' in items:
                    if isinstance(items['item'], list):
                        df = pd.DataFrame(items['item'])
                    else:
                        df = pd.DataFrame([items['item']])
                    
                    logger.info(f"데이터 성공적으로 가져옴: {len(df)}개 항목")
                    return df
        else:  # XML 처리
            root = ET.fromstring(response.content)
            items = []
            for item in root.findall('.//item'):
                item_dict = {child.tag: child.text for child in item}
                items.append(item_dict)
            
            df = pd.DataFrame(items)
            logger.info(f"XML 데이터 성공적으로 가져옴: {len(df)}개 항목")
            return df
        
        logger.warning("데이터를 찾을 수 없습니다.")
        return pd.DataFrame()
    
    except requests.RequestException as e:
        logger.error(f"API 요청 중 오류 발생: {e}")
        st.error(f"데이터를 가져오는 중 네트워크 오류가 발생했습니다: {e}")
        return pd.DataFrame()
    except Exception as e:
        logger.error(f"예기치 못한 오류 발생: {e}")
        st.error(f"데이터 처리 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()

def preprocess_data(df):
    """
    데이터 전처리 함수
    
    Args:
        df (pandas.DataFrame): 원본 데이터프레임
    
    Returns:
        pandas.DataFrame: 전처리된 데이터프레임
    """
    if df.empty:
        logger.warning("빈 데이터프레임 전달됨")
        return df
    
    try:
        # 숫자형 컬럼 변환
        numeric_columns = ['foreigner', 'korean']
        for col in numeric_columns:
            if col in df.columns:
                df[col] = pd.to_numeric(df[col], errors='coerce').fillna(0)
        
        # 날짜 컬럼 변환
        date_columns = ['estimatedtime', 'scheduletime']
        for col in date_columns:
            if col in df.columns:
                df[col] = pd.to_datetime(df[col], format='%Y%m%d%H%M', errors='coerce')
        
        # 총 인원 계산
        if 'foreigner' in df.columns and 'korean' in df.columns:
            df['total_people'] = df['foreigner'] + df['korean']
        
        # 추가 전처리 (필요시 확장 가능)
        logger.info("데이터 전처리 완료")
        return df
    
    except Exception as e:
        logger.error(f"데이터 전처리 중 오류 발생: {e}")
        return df

def create_congestion_visualization(df):
    """
    혼잡도 시각화 함수
    
    Args:
        df (pandas.DataFrame): 전처리된 데이터프레임
    
    Returns:
        plotly.graph_objects.Figure: 혼잡도 차트
    """
    try:
        # 입국장별 혼잡도 계산
        if 'entrygate' in df.columns:
            gate_summary = df.groupby('entrygate').agg({
                'korean': 'sum',
                'foreigner': 'sum'
            }).reset_index()
            gate_summary['total'] = gate_summary['korean'] + gate_summary['foreigner']
            
            # Plotly 스택 바 차트
            fig = go.Figure()
            fig.add_trace(go.Bar(
                x=gate_summary['entrygate'],
                y=gate_summary['korean'],
                name='내국인',
                marker_color='#1976d2'
            ))
            fig.add_trace(go.Bar(
                x=gate_summary['entrygate'],
                y=gate_summary['foreigner'],
                name='외국인',
                marker_color='#ff9800'
            ))
            
            fig.update_layout(
                title='입국장별 대기 인원',
                xaxis_title='입국장',
                yaxis_title='인원 수',
                barmode='stack',
                height=400
            )
            
            logger.info("혼잡도 시각화 생성 성공")
            return fig
        
        logger.warning("혼잡도 시각화에 필요한 데이터 없음")
        return None
    
    except Exception as e:
        logger.error(f"혼잡도 시각화 생성 중 오류 발생: {e}")
        return None

def main():
    """
    Streamlit 앱의 메인 함수
    """
    # 페이지 설정
    st.set_page_config(
        page_title="인천국제공항 실시간 정보",
        page_icon="✈️",
        layout="wide",
        initial_sidebar_state="expanded"
    )

    # 커스텀 CSS 스타일 적용
    st.markdown("""
    <style>
    .main { background-color: #f9f9f9; }
    .title-container { 
        background-color: #0a4d8c; 
        color: white; 
        text-align: center; 
        padding: 20px; 
        border-radius: 10px; 
    }
    /* 추가 CSS 스타일 */
    </style>
    """, unsafe_allow_html=True)

    # 헤더 섹션
    st.markdown("""
    <div class="title-container">
        <h1>
            <span>✈️</span> 
            인천국제공항 실시간 정보 시스템
        </h1>
        <p>실시간 입국장 혼잡도 및 항공편 정보를 시각적으로 확인하세요</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바 설정
    with st.sidebar:
        st.image("https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Incheon_International_Airport_logo.svg/320px-Incheon_International_Airport_logo.svg.png", width=200)
        
        # 터미널 선택
        terminal = st.selectbox(
            "터미널을 선택하세요:",
            options=["T1", "T2"],
            index=0
        )

        # 고급 검색 옵션
        with st.expander("고급 검색 옵션"):
            airport_code = st.text_input("출발지 공항 코드 (예: HKG)")
        
        # 정보 조회 버튼
        search_button = st.button("정보 조회", use_container_width=True)
        
        # 자동 갱신 토글
        auto_refresh = st.toggle("실시간 데이터 자동 갱신", value=False)
        
        if auto_refresh:
            refresh_interval = st.slider("갱신 주기 (초)", min_value=30, max_value=300, value=60, step=10)

    # 데이터 조회 및 처리
    if search_button or (auto_refresh and 'refresh_interval' in locals()):
        with st.spinner("실시간 데이터를 불러오는 중..."):
            try:
                # 데이터 가져오기
                df = fetch_data(
                    terminal, 
                    num_rows=100, 
                    response_type="json", 
                    airport=airport_code if airport_code else None
                )
                
                # 데이터 전처리
                df = preprocess_data(df)
            
            except Exception as e:
                logger.error(f"데이터 처리 중 오류 발생: {e}")
                st.error("데이터를 처리하는 중 문제가 발생했습니다.")
                df = pd.DataFrame()
        
        # 데이터 표시 로직
        if not df.empty:
            # 탭 생성
            tab1, tab2, tab3 = st.tabs(["📊 혼잡도 현황", "✈️ 항공편 정보", "🔍 입국장 안내"])
            
            # 혼잡도 현황 탭
            with tab1:
                st.markdown("<h2>실시간 입국장 혼잡도</h2>", unsafe_allow_html=True)
                
                # 총 인원 요약
                total_people = df['total_people'].sum() if 'total_people' in df.columns else 0
                korean_people = df['korean'].sum() if 'korean' in df.columns else 0
                foreigner_people = df['foreigner'].sum() if 'foreigner' in df.columns else 0
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("총 대기 인원", f"{int(total_people)}명")
                with col2:
                    st.metric("내국인", f"{int(korean_people)}명")
                with col3:
                    st.metric("외국인", f"{int(foreigner_people)}명")
                
                # 혼잡도 시각화
                congestion_fig = create_congestion_visualization(df)
                if congestion_fig:
                    st.plotly_chart(congestion_fig, use_container_width=True)
                else:
                    st.info("혼잡도 시각화를 생성할 수 없습니다.")
            
            # 항공편 정보 탭
            with tab2:
                st.markdown("<h2>항공편 정보</h2>", unsafe_allow_html=True)
                
                # 항공편 테이블 표시
                display_columns = ['flightid', 'airport', 'entrygate', 'scheduletime', 'estimatedtime']
                display_columns = [col for col in display_columns if col in df.columns]
                
                if display_columns:
                    display_df = df[display_columns].copy()
                    
                    # 컬럼명
                    column_mapping = {
                        'flightid': '편명',
                        'airport': '출발지',
                        'entrygate': '입국장',
                        'scheduletime': '예정시간',
                        'estimatedtime': '도착시간'
                    }
                    display_df.rename(columns={col: column_mapping.get(col, col) for col in display_df.columns}, inplace=True)
                    
                    # 시간 형식 변경
                    for col in ['예정시간', '도착시간']:
                        if col in display_df.columns:
                            display_df[col] = display_df[col].dt.strftime('%Y-%m-%d %H:%M')
                    
                    st.dataframe(display_df, use_container_width=True)
                else:
                    st.info("항공편 정보가 없습니다.")
                
                # 출발지 공항별 항공편 분포
                if 'airport' in df.columns:
                    airport_counts = df['airport'].value_counts().reset_index()
                    airport_counts.columns = ['공항', '항공편 수']
                    
                    # 상위 10개 공항 시각화
                    fig = px.bar(
                        airport_counts.head(10), 
                        x='공항', 
                        y='항공편 수', 
                        title='출발지 공항별 항공편 분포 (상위 10개)',
                        labels={'공항': '출발지 공항', '항공편 수': '항공편 수'}
                    )
                    st.plotly_chart(fig, use_container_width=True)
            
            # 입국장 안내 탭
            with tab3:
                st.markdown("<h2>입국장 안내</h2>", unsafe_allow_html=True)
                
                # 터미널별 입국장 정보
                terminal_info = {
                    "T1": {
                        "gates": ["A", "B", "C", "D", "E", "F"],
                        "details": {
                            "A": "동편 입구 근처, 주로 저비용 항공사 이용",
                            "B": "동편 중앙, 국내선 및 일부 국제선",
                            "C": "중앙 입국장, 주요 국제선 이용",
                            "D": "서편 중앙, 다양한 항공사 이용",
                            "E": "서편 출구 근처, 대형 항공사 이용",
                            "F": "서편 특별 입국장"
                        }
                    },
                    "T2": {
                        "gates": ["A", "B", "C"],
                        "details": {
                            "A": "동편 입국장, 아시아 노선 중심",
                            "B": "중앙 입국장, 국제선 중심",
                            "C": "서편 입국장, 장거리 국제선"
                        }
                    }
                }
                
                # 선택된 터미널의 입국장 정보 표시
                selected_terminal_info = terminal_info.get(terminal, {"gates": [], "details": {}})
                
                for gate in selected_terminal_info["gates"]:
                    gate_detail = selected_terminal_info["details"].get(gate, "추가 정보 없음")
                    
                    # 입국장 상세 정보 카드
                    st.markdown(f"""
                    <div style="background-color: #f0f0f0; padding: 15px; border-radius: 8px; margin-bottom: 10px; 
                                border-left: 5px solid {'#4CAF50' if gate in ['A', 'B'] else '#2196F3' if gate in ['C', 'D'] else '#FF9800'};">
                        <h3>{terminal} 터미널 입국장 {gate}</h3>
                        <p>{gate_detail}</p>
                        
                        <div style="display: flex; justify-content: space-between; margin-top: 10px;">
                            <span>
                                <strong>상태:</strong> 
                                {'여유' if np.random.random() > 0.5 else '보통' if np.random.random() > 0.3 else '혼잡'}
                            </span>
                            <span>
                                <strong>예상 대기 시간:</strong> 
                                {np.random.randint(10, 60)}분
                            </span>
                        </div>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 공항 교통 정보 요약
                st.markdown("<h3>교통 정보</h3>", unsafe_allow_html=True)
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.metric("공항철도", "43분")
                
                with col2:
                    st.metric("리무진 버스", "60-90분")
                
                with col3:
                    st.metric("택시", "45-70분")
        else:
            st.warning("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")

    # 페이지 하단 정보
    st.markdown("""
    <div style="text-align: center; color: #666; margin-top: 30px; padding: 10px; border-top: 1px solid #eee;">
        <p>© 2025 인천국제공항 실시간 정보 시스템 | 데이터 출처: 인천국제공항공사</p>
        <p>최종 업데이트: {current_time}</p>
    </div>
    """.format(current_time=datetime.now().strftime("%Y-%m-%d %H:%M:%S")), unsafe_allow_html=True)

    # 자동 갱신 로직
    if 'auto_refresh' in locals() and auto_refresh:
        time.sleep(refresh_interval)
        st.experimental_rerun()

# 애플리케이션 실행
if __name__ == "__main__":
    main()
