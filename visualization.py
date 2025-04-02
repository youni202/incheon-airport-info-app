import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from app_functions import get_congestion_level

# 입국장별 혼잡도 차트 생성
def create_congestion_chart(df):
    if 'entrygate' in df.columns and 'korean' in df.columns and 'foreigner' in df.columns:
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
        
        return fig, gate_summary
    
    return None, None

# 시간대별 항공편 차트 생성
def create_hourly_flight_chart(df):
    if 'estimatedtime' in df.columns:
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
        
        return fig
    
    return None

# 공항별 항공편 차트 생성
def create_airport_chart(df):
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
        
        return fig
    
    return None

# 혼잡도 상태 표시
def display_congestion_status(gate_summary):
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