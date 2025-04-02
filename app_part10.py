# 공항 교통 정보
            st.markdown("<h3>공항 교통 정보</h3>", unsafe_allow_html=True)
            
            transport_tab1, transport_tab2, transport_tab3 = st.tabs(["공항철도", "버스", "택시/승용차"])
            
            with transport_tab1:
                st.markdown("""
                <div class="card">
                    <h4>공항철도 안내</h4>
                    <p><strong>운행시간:</strong> 첫차 05:20 - 막차 24:00 (평일 기준)</p>
                    <p><strong>소요시간:</strong> 인천공항 - 서울역 약 43분 (직통열차)</p>
                    <p><strong>요금:</strong> 일반열차 4,150원, 직통열차 9,000원</p>
                    
                    <h5>주요 정차역</h5>
                    <ul>
                        <li>인천공항 제2터미널 - 인천공항 제1터미널 - 검암 - 계양 - 디지털미디어시티 - 홍대입구 - 서울역</li>
                    </ul>
                </div>
                """, unsafe_allow_html=True)
            
            with transport_tab2:
                st.markdown("""
                <div class="card">
                    <h4>공항 리무진 버스</h4>
                    <p>인천공항에서 서울 및 수도권 각 지역을 연결하는 리무진 버스가 운행됩니다.</p>
                    
                    <h5>주요 노선</h5>
                    <ul>
                        <li><strong>6001번:</strong> 인천공항 - 강남역</li>
                        <li><strong>6002번:</strong> 인천공항 - 강남역 - 양재역 - 강남고속터미널</li>
                        <li><strong>6015번:</strong> 인천공항 - 홍대입구 - 신촌 - 이대</li>
                        <li><strong>6701번:</strong> 인천공항 - 부천 - 광명</li>
                    </ul>
                    
                    <p><strong>요금:</strong> 노선에 따라 약 10,000원 ~ 18,000원</p>
                    <p><strong>운행시간:</strong> 첫차 04:30 - 막차 22:40 (노선에 따라 다름)</p>
                </div>
                """, unsafe_allow_html=True)
            
            with transport_tab3:
                st.markdown("""
                <div class="card">
                    <h4>택시 및 승용차</h4>
                    <p><strong>일반택시:</strong> 미터기 요금 (서울까지 약 65,000원 ~ 100,000원)</p>
                    <p><strong>모범택시:</strong> 미터기 요금 (서울까지 약 100,000원 ~ 150,000원)</p>
                    <p><strong>국제택시:</strong> 외국인 전용 예약 택시 서비스 (영어, 일본어, 중국어 가능)</p>
                    
                    <h5>주차 정보</h5>
                    <p><strong>제1터미널 주차장:</strong> 2,500면</p>
                    <p><strong>제2터미널 주차장:</strong> 2,000면</p>
                    <p><strong>주차요금:</strong> 기본 30분 2,500원, 추가 10분당 1,000원</p>
                </div>
                """, unsafe_allow_html=True)
    else:
        st.warning("데이터를 불러올 수 없습니다. 잠시 후 다시 시도해주세요.")

# 푸터
st.markdown("""
<div class="footer">
    <p>© 2025 인천국제공항 실시간 정보 시스템 | 데이터 출처: 인천국제공항공사</p>
    <p>이 앱은 공공데이터포털 API를 활용하여 제작되었습니다.</p>
</div>
""", unsafe_allow_html=True)

# 자동 갱신 로직
if auto_refresh:
    time.sleep(refresh_interval)
    st.experimental_rerun()