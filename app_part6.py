# 항공편 목록 표시
            
            # 모든 항공편 목록 표시
            st.markdown("<h3>오늘의 도착 항공편</h3>", unsafe_allow_html=True)
            
            if not df.empty:
                # 컬럼 정리 및 이름 변경
                display_columns = ['flightid', 'airport', 'entrygate', 'gatenumber', 'scheduletime', 'estimatedtime']
                display_columns = [col for col in display_columns if col in df.columns]
                
                if display_columns:
                    display_df = df[display_columns].copy()
                    
                    column_mapping = {
                        'flightid': '편명',
                        'airport': '출발지',
                        'entrygate': '입국장',
                        'gatenumber': '게이트',
                        'scheduletime': '예정시간',
                        'estimatedtime': '도착시간'
                    }
                    
                    display_df.rename(columns={col: column_mapping.get(col, col) for col in display_df.columns}, inplace=True)
                    
                    # 시간 형식 변경
                    for col in ['예정시간', '도착시간']:
                        if col in display_df.columns:
                            display_df[col] = display_df[col].dt.strftime('%H:%M')
                    
                    # 항공편 목록 표시
                    st.dataframe(display_df.sort_values('예정시간' if '예정시간' in display_df.columns else '편명'), use_container_width=True)
                else:
                    st.info("항공편 정보를 불러올 수 없습니다.")
            else:
                st.info("항공편 정보가 없습니다.")
            
            # 출발지 공항별 도착 항공편 수 시각화
            if 'airport' in df.columns:
                airport_counts = df['airport'].value_counts().reset_index()
                airport_counts.columns = ['공항', '항공편수']
                
                # 상위 10개 공항만 표시
                top_airports = airport_counts.head(10)
                
                # Plotly로 공항별 항공편 차트
                fig = px.bar(
                    top_airports,
                    x='공항',
                    y='항공편수',
                    color='항공편수',
                    color_continuous_scale='Blues',
                    title='출발지 공항별 도착 항공편 수 (상위 10개)',
                    height=400
                )
                
                fig.update_layout(
                    xaxis_title='출발지 공항',
                    yaxis_title='항공편 수',
                    coloraxis_showscale=False,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)