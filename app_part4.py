# 메인 콘텐츠 영역 - 시간대별 항공편 차트
        
            # 시간대별 항공편 도착 차트
            if 'estimatedtime' in df.columns:
                st.markdown("<h3>시간대별 도착 항공편</h3>", unsafe_allow_html=True)
                
                df['hour'] = df['estimatedtime'].dt.hour
                flight_by_hour = df.groupby('hour').size().reset_index(name='count')
                
                # Plotly로 시간대별 항공편 차트
                fig = px.line(
                    flight_by_hour, 
                    x='hour', 
                    y='count',
                    markers=True,
                    line_shape='spline',
                    title='시간대별 도착 항공편 수',
                    labels={'hour': '시간', 'count': '항공편 수'}
                )
                
                fig.update_traces(line=dict(color='#1976d2', width=3))
                fig.update_layout(
                    xaxis=dict(
                        tickmode='linear',
                        tick0=0,
                        dtick=1
                    ),
                    height=400,
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
        
        # 탭 2: 항공편 정보
        with tab2:
            st.markdown("""
            <div class="card">
                <h2>항공편 정보 및 검색</h2>
                <p>도착 예정 항공편 정보를 확인하고 편명 또는 출발지로 검색할 수 있습니다.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 항공편 검색 기능
            search_col1, search_col2, search_col3 = st.columns([2, 2, 1])
            
            with search_col1:
                search_flight = st.text_input("편명 검색 (예: KE123)", key="flight_search")
            
            with search_col2:
                search_airport = st.text_input("출발지 공항 검색 (예: HKG)", key="airport_search")
            
            with search_col3:
                st.markdown("<br>", unsafe_allow_html=True)
                search_btn = st.button("검색", use_container_width=True)