# 메인 콘텐츠 영역 - 첫 번째 부분
# 메인 콘텐츠 영역
if search_button or auto_refresh:
    # 로딩 스피너
    with st.spinner("실시간 데이터를 불러오는 중..."):
        df = fetch_data(terminal, num_rows=100, response_type="json", airport=airport_code if airport_code else None)
        df = preprocess_data(df)
    
    if not df.empty:
        # 탭 네비게이션
        tab1, tab2, tab3 = st.tabs(["📊 혼잡도 현황", "✈️ 항공편 정보", "🔍 입국장 안내"])
        
        # 탭 1: 혼잡도 현황
        with tab1:
            st.markdown("""
            <div class="card">
                <h2>실시간 입국장 혼잡도</h2>
                <p>각 입국장별 현재 대기 인원 및 혼잡 상태를 확인하세요.</p>
            </div>
            """, unsafe_allow_html=True)
            
            # 요약 정보 카드
            if 'korean' in df.columns and 'foreigner' in df.columns:
                total_korean = df['korean'].sum()
                total_foreigner = df['foreigner'].sum()
                total_people = total_korean + total_foreigner
                
                col1, col2, col3 = st.columns(3)
                
                with col1:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{int(total_people)}</div>
                        <div class="metric-label">총 대기 인원</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col2:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{int(total_korean)}</div>
                        <div class="metric-label">내국인</div>
                    </div>
                    """, unsafe_allow_html=True)
                
                with col3:
                    st.markdown(f"""
                    <div class="metric-card">
                        <div class="metric-value">{int(total_foreigner)}</div>
                        <div class="metric-label">외국인</div>
                    </div>
                    """, unsafe_allow_html=True)
            
            # 입국장별 혼잡도 차트
            if 'entrygate' in df.columns:
                st.markdown("<h3>입국장별 대기 인원</h3>", unsafe_allow_html=True)
                
                gate_summary = df.groupby('entrygate').agg({
                    'korean': 'sum',
                    'foreigner': 'sum'
                }).reset_index()
                
                gate_summary['total'] = gate_summary['korean'] + gate_summary['foreigner']
                
                # Plotly로 대화형 바 차트
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
                    height=500,
                    template='plotly_white',
                    legend=dict(
                        orientation="h",
                        yanchor="bottom",
                        y=1.02,
                        xanchor="right",
                        x=1
                    ),
                    margin=dict(l=20, r=20, t=40, b=20)
                )
                
                st.plotly_chart(fig, use_container_width=True)
                
                # 혼잡도 수준 계산 및 표시
                def get_congestion_level(count):
                    if count < 50:
                        return "여유", "#4CAF50"  # 녹색
                    elif count < 100:
                        return "보통", "#FFC107"  # 노란색
                    else:
                        return "혼잡", "#F44336"  # 빨간색
                
                st.markdown("<h3>입국장별 혼잡도 상태</h3>", unsafe_allow_html=True)
                
                congestion_cols = st.columns(len(gate_summary))
                
                for i, (_, gate_data) in enumerate(gate_summary.iterrows()):
                    level, color = get_congestion_level(gate_data['total'])
                    
                    with congestion_cols[i]:
                        st.markdown(f"""
                        <div style="background-color: {color}; color: white; padding: 15px; border-radius: 8px; text-align: center;">
                            <h2 style="margin: 0;">{gate_data['entrygate']}</h2>
                            <div style="font-size: 24px; font-weight: bold;">{int(gate_data['total'])}</div>
                            <div>{level}</div>
                        </div>
                        """, unsafe_allow_html=True)