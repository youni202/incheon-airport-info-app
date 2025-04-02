# T2 정보
            with terminal_tab2:
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("<h3>제2터미널 입국장 위치</h3>", unsafe_allow_html=True)
                    
                    # 입국장 정보 카드
                    for gate, description in entry_info["T2"].items():
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #0a4d8c; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: #0a4d8c;">입국장 {gate}</h4>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<h3>제2터미널 층별 안내</h3>", unsafe_allow_html=True)
                    
                    # 층별 안내
                    floors = {
                        "4층": "식당가, 면세점, 전망대",
                        "3층": "출국장, 체크인 카운터, 면세점",
                        "2층": "출국 심사대, 면세점, 라운지",
                        "1층": "입국장, 입국 심사대, 수하물 수취대",
                        "B1층": "교통 센터, 지하철, 버스 터미널, 환승 열차"
                    }
                    
                    for floor, description in floors.items():
                        st.markdown(f"""
                        <div style="background-color: #f5f5f5; padding: 10px; border-radius: 8px; margin-bottom: 10px;">
                            <h4 style="margin: 0; color: #0a4d8c;">{floor}</h4>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                    
                    # 공항 연락처 정보
                    st.markdown("""
                    <div style="background-color: #e1f5fe; padding: 15px; border-radius: 8px; margin-top: 20px; border-left: 5px solid #039be5;">
                        <h4 style="margin-top: 0;">공항 안내 연락처</h4>
                        <p>☎ 1577-2600</p>
                        <p>✉ cip@airport.kr</p>
                    </div>
                    """, unsafe_allow_html=True)
                
                # 항공사 카운터 정보
                st.markdown("<h3>제2터미널 주요 항공사 카운터</h3>", unsafe_allow_html=True)
                
                # 항공사 표 생성
                airline_data = []
                for airline, info in airline_counters["T2"].items():
                    airline_data.append({
                        "항공사": airline,
                        "카운터 위치": info["카운터"],
                        "가까운 입구": info["입구"],
                        "연결 입국장": info["연결 입국장"]
                    })
                
                airline_df = pd.DataFrame(airline_data)
                st.dataframe(airline_df, use_container_width=True)
                
                # 간단한 터미널 맵 (스타일링된 레이아웃)
                st.markdown("<h3>제2터미널 간략 맵</h3>", unsafe_allow_html=True)
                
                st.markdown("""
                <div style="background-color: #f5f5f5; padding: 20px; border-radius: 8px; text-align: center;">
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                        <div style="background-color: #90caf9; padding: 15px; border-radius: 8px; width: 30%;">동편</div>
                        <div style="background-color: #90caf9; padding: 15px; border-radius: 8px; width: 30%;">중앙</div>
                        <div style="background-color: #90caf9; padding: 15px; border-radius: 8px; width: 30%;">서편</div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between; margin-bottom: 20px;">
                        <div style="width: 30%; text-align: center;">
                            <div style="background-color: #4fc3f7; padding: 10px; border-radius: 8px;">입국장 A</div>
                        </div>
                        <div style="width: 30%; text-align: center;">
                            <div style="background-color: #4fc3f7; padding: 10px; border-radius: 8px;">입국장 B</div>
                        </div>
                        <div style="width: 30%; text-align: center;">
                            <div style="background-color: #4fc3f7; padding: 10px; border-radius: 8px;">입국장 C</div>
                        </div>
                    </div>
                    
                    <div style="display: flex; justify-content: space-between;">
                        <div style="background-color: #81c784; padding: 10px; border-radius: 8px; width: 30%;">1번 출구</div>
                        <div style="background-color: #81c784; padding: 10px; border-radius: 8px; width: 30%;">2번 출구</div>
                        <div style="background-color: #81c784; padding: 10px; border-radius: 8px; width: 30%;">3번 출구</div>
                    </div>
                </div>
                """, unsafe_allow_html=True)