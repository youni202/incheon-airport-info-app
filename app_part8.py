# T1 정보
            with terminal_tab1:
                col1, col2 = st.columns([3, 2])
                
                with col1:
                    st.markdown("<h3>제1터미널 입국장 위치</h3>", unsafe_allow_html=True)
                    
                    # 입국장 정보 카드
                    for gate, description in entry_info["T1"].items():
                        st.markdown(f"""
                        <div style="background-color: white; padding: 15px; border-radius: 8px; margin-bottom: 10px; border-left: 5px solid #0a4d8c; box-shadow: 0 2px 4px rgba(0,0,0,0.1);">
                            <h4 style="margin: 0; color: #0a4d8c;">입국장 {gate}</h4>
                            <p>{description}</p>
                        </div>
                        """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown("<h3>제1터미널 층별 안내</h3>", unsafe_allow_html=True)
                    
                    # 층별 안내
                    floors = {
                        "4층": "식당가, 면세점, 라운지",
                        "3층": "출국장, 체크인 카운터, 면세점",
                        "2층": "출국 심사대, 면세점",
                        "1층": "입국장, 입국 심사대, 수하물 수취대",
                        "B1층": "교통 센터, 지하철, 버스 터미널"
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
                st.markdown("<h3>제1터미널 주요 항공사 카운터</h3>", unsafe_allow_html=True)
                
                # 항공사 표 생성
                airline_data = []
                for airline, info in airline_counters["T1"].items():
                    airline_data.append({
                        "항공사": airline,
                        "카운터 위치": info["카운터"],
                        "가까운 입구": info["입구"],
                        "연결 입국장": info["연결 입국장"]
                    })
                
                airline_df = pd.DataFrame(airline_data)
                
                # 스타일링된 테이블
                st.markdown("""
                <style>
                .airline-table {
                    font-size: 14px;
                    border-collapse: collapse;
                    width: 100%;
                }
                .airline-table th {
                    background-color: #0a4d8c;
                    color: white;
                    text-align: left;
                    padding: 12px;
                }
                .airline-table td {
                    padding: 12px;
                    border-bottom: 1px solid #ddd;
                }
                .airline-table tr:nth-child(even) {
                    background-color: #f9f9f9;
                }
                .airline-table tr:hover {
                    background-color: #f1f1f1;
                }
                </style>
                """, unsafe_allow_html=True)
                
                st.dataframe(airline_df, use_container_width=True)