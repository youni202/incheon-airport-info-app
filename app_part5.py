# 항공편 검색 결과 표시 부분
            
            if search_btn or search_flight or search_airport:
                search_results = df.copy()
                
                if search_flight:
                    search_results = search_results[search_results['flightid'].str.contains(search_flight, case=False, na=False)]
                
                if search_airport:
                    search_results = search_results[search_results['airport'].str.contains(search_airport, case=False, na=False)]
                
                if not search_results.empty:
                    st.success(f"{len(search_results)}개의 항공편이 검색되었습니다.")
                    
                    # 검색 결과 테이블로 표시
                    result_columns = ['flightid', 'airport', 'entrygate', 'gatenumber', 'scheduletime', 'estimatedtime', 'korean', 'foreigner']
                    result_columns = [col for col in result_columns if col in search_results.columns]
                    
                    if result_columns:
                        result_df = search_results[result_columns].copy()
                        
                        # 컬럼명 변경
                        column_mapping = {
                            'flightid': '편명',
                            'airport': '출발지',
                            'entrygate': '입국장',
                            'gatenumber': '게이트',
                            'scheduletime': '예정시간',
                            'estimatedtime': '도착시간',
                            'korean': '내국인',
                            'foreigner': '외국인'
                        }
                        
                        result_df.rename(columns={col: column_mapping.get(col, col) for col in result_df.columns}, inplace=True)
                        
                        # 스타일링된 테이블
                        st.markdown("""
                        <style>
                        .dataframe {
                            font-size: 14px;
                            border-collapse: collapse;
                            width: 100%;
                        }
                        .dataframe th {
                            background-color: #0a4d8c;
                            color: white;
                            text-align: left;
                            padding: 12px;
                        }
                        .dataframe td {
                            padding: 12px;
                            border-bottom: 1px solid #ddd;
                        }
                        .dataframe tr:nth-child(even) {
                            background-color: #f9f9f9;
                        }
                        .dataframe tr:hover {
                            background-color: #f1f1f1;
                        }
                        </style>
                        """, unsafe_allow_html=True)
                        
                        st.dataframe(result_df, use_container_width=True)
                        
                        # 입국장 안내
                        if 'entrygate' in search_results.columns and not search_results['entrygate'].isna().all():
                            entry_gate = search_results.iloc[0]['entrygate']
                            flight_id = search_results.iloc[0]['flightid']
                            
                            st.markdown(f"""
                            <div class="info-box">
                                <h4>항공편 안내</h4>
                                <p>편명 <b>{flight_id}</b>의 여객은 <b>입국장 {entry_gate}</b>를 이용하세요.</p>
                            </div>
                            """, unsafe_allow_html=True)
                else:
                    st.warning("검색 결과가 없습니다.")