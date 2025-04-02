# 사이드바 디자인
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