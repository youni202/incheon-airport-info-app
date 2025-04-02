import streamlit as st
import pandas as pd
from datetime import datetime

# 사이드바 구성 함수
def create_sidebar():
    st.sidebar.markdown("""
    <div style="text-align: center; padding: 10px;">
        <img src="https://upload.wikimedia.org/wikipedia/commons/thumb/0/0f/Incheon_International_Airport_logo.svg/320px-Incheon_International_Airport_logo.svg.png" width="200">
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='text-align: center;'>실시간 정보 조회</h2>", unsafe_allow_html=True)

    # 사이드바 - 터미널 선택
    terminal = st.sidebar.selectbox(
        "터미널을 선택하세요:",
        options=["T1", "T2"],
        index=0
    )

    # 고급 검색 옵션
    with st.sidebar.expander("고급 검색 옵션"):
        airport_code = st.text_input("출발지 공항 코드 (예: HKG)")
        
        st.markdown("""
        **주요 공항 코드:**
        - HKG: 홍콩
        - NRT: 도쿄 나리타
        - LAX: 로스앤젤레스
        - JFK: 뉴욕
        - LHR: 런던 히드로
        - CDG: 파리 샤를드골
        """)

    # 사이드바 - 정보 조회 버튼
    search_button = st.sidebar.button("정보 조회", use_container_width=True)

    # 실시간 데이터 표시 스위치
    auto_refresh = st.sidebar.toggle("실시간 데이터 자동 갱신", value=False)
    if auto_refresh:
        refresh_interval = st.sidebar.slider("갱신 주기 (초)", min_value=30, max_value=300, value=60, step=10)
        st.sidebar.markdown(f"""
        <div class="info-box">
            <span class="live-indicator"></span> 실시간 데이터가 {refresh_interval}초마다 갱신됩니다.
        </div>
        """, unsafe_allow_html=True)
    else:
        refresh_interval = 60  # 기본값

    # 현재 시간 표시
    current_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    st.sidebar.markdown(f"""
    <div style="text-align: center; padding: 10px; background-color: #f0f2f6; border-radius: 8px; margin-top: 20px;">
        <p>현재 시간: {current_time}</p>
    </div>
    """, unsafe_allow_html=True)

    # 사이드바 푸터
    st.sidebar.markdown("""
    <div class="footer">
        <p>이 앱은 인천국제공항공사의 공공데이터 API를 활용하여 제작되었습니다.</p>
        <p>© 2025 인천공항 정보 서비스</p>
    </div>
    """, unsafe_allow_html=True)
    
    return terminal, airport_code, search_button, auto_refresh, refresh_interval

# 공항 정보 데이터
def get_airport_info():
    # 입국장 정보
    entry_info = {
        "T1": {
            "A": "1층 A 입국장 - 동편 출구 근처",
            "B": "1층 B 입국장 - 동편 중앙 근처",
            "C": "1층 C 입국장 - 중앙 근처",
            "D": "1층 D 입국장 - 서편 중앙 근처",
            "E": "1층 E 입국장 - 서편 출구 근처",
            "F": "1층 F 입국장 - 서편 특별 입국장"
        },
        "T2": {
            "A": "1층 A 입국장 - 동편",
            "B": "1층 B 입국장 - 중앙",
            "C": "1층 C 입국장 - 서편"
        }
    }
    
    # 항공사 카운터 정보
    airline_counters = {
        "T1": {
            "대한항공(KE)": {"카운터": "M 카운터 (3층 중앙)", "입구": "1번, 2번, 3번", "연결 입국장": "B, C"},
            "아시아나항공(OZ)": {"카운터": "F 카운터 (3층 서편)", "입구": "4번, 5번", "연결 입국장": "D, E"},
            "제주항공(7C)": {"카운터": "D 카운터 (3층 동편)", "입구": "6번, 7번", "연결 입국장": "A, B"},
            "진에어(LJ)": {"카운터": "G 카운터 (3층 중앙)", "입구": "3번, 4번", "연결 입국장": "C, D"},
            "티웨이항공(TW)": {"카운터": "B 카운터 (3층 동편)", "입구": "7번, 8번", "연결 입국장": "A"},
            "에어서울(RS)": {"카운터": "H 카운터 (3층 중앙)", "입구": "4번, 5번", "연결 입국장": "C, D"},
            "이스타항공(ZE)": {"카운터": "C 카운터 (3층 동편)", "입구": "6번, 7번", "연결 입국장": "B"},
            "에어부산(BX)": {"카운터": "I 카운터 (3층 중앙)", "입구": "4번, 5번", "연결 입국장": "C, D"},
            "플라이강원(4V)": {"카운터": "J 카운터 (3층 중앙)", "입구": "3번, 4번", "연결 입국장": "C"}
        },
        "T2": {
            "대한항공(KE)": {"카운터": "240-280 카운터 (3층 중앙)", "입구": "1번, 2번", "연결 입국장": "A, B"},
            "델타항공(DL)": {"카운터": "210-230 카운터 (3층 동편)", "입구": "1번", "연결 입국장": "A"},
            "에어프랑스(AF)": {"카운터": "310-330 카운터 (3층 서편)", "입구": "3번", "연결 입국장": "C"},
            "KLM(KL)": {"카운터": "290-300 카운터 (3층 서편)", "입구": "3번", "연결 입국장": "C"},
            "케세이퍼시픽(CX)": {"카운터": "230-250 카운터 (3층 동편)", "입구": "1번, 2번", "연결 입국장": "A"},
            "중국동방항공(MU)": {"카운터": "340-350 카운터 (3층 서편)", "입구": "3번", "연결 입국장": "C"},
            "중국남방항공(CZ)": {"카운터": "350-370 카운터 (3층 서편)", "입구": "3번", "연결 입국장": "C"},
            "샤먼항공(MF)": {"카운터": "370-380 카운터 (3층 서편)", "입구": "2번, 3번", "연결 입국장": "B, C"}
        }
    }
    
    return entry_info, airline_counters