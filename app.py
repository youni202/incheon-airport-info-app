import streamlit as st
import pandas as pd
import numpy as np
import requests
import matplotlib.pyplot as plt
import seaborn as sns
import xml.etree.ElementTree as ET
import json
from datetime import datetime, timedelta
import time
import plotly.express as px
import plotly.graph_objects as go
from PIL import Image
import base64

# 페이지 설정
st.set_page_config(
    page_title="인천국제공항 실시간 정보",
    page_icon="✈️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# 사용자 정의 CSS 스타일 적용
st.markdown("""
<style>
    /* 전체 앱 스타일 */
    .main {
        background-color: #f9f9f9;
        padding: 20px;
    }
    
    /* 헤더 스타일 */
    .title-container {
        background-color: #0a4d8c;
        padding: 20px;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin-bottom: 20px;
    }
    
    /* 카드 스타일 */
    .card {
        background-color: white;
        padding: 20px;
        border-radius: 10px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.1);
        margin-bottom: 20px;
    }
    
    /* 정보 박스 스타일 */
    .info-box {
        background-color: #e1f5fe;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #039be5;
        margin-bottom: 15px;
    }
    
    /* 경고 박스 스타일 */
    .warning-box {
        background-color: #fff8e1;
        padding: 15px;
        border-radius: 8px;
        border-left: 5px solid #ffc107;
        margin-bottom: 15px;
    }
    
    /* 메트릭 스타일 */
    .metric-container {
        display: flex;
        justify-content: space-between;
        margin-bottom: 20px;
    }
    
    .metric-card {
        background-color: white;
        padding: 15px;
        border-radius: 8px;
        box-shadow: 0 2px 4px rgba(0, 0, 0, 0.1);
        text-align: center;
        flex: 1;
        margin: 0 5px;
    }
    
    .metric-value {
        font-size: 28px;
        font-weight: bold;
        color: #0a4d8c;
    }
    
    .metric-label {
        font-size: 14px;
        color: #666;
    }
    
    /* 탭 스타일 */
    .stTabs [data-baseweb="tab-list"] {
        gap: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        background-color: #f1f1f1;
        border-radius: 8px 8px 0 0;
        padding: 10px 20px;
        height: 50px;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #0a4d8c;
        color: white;
    }
    
    /* 테이블 스타일 */
    .dataframe {
        width: 100%;
        font-size: 14px;
    }
    
    /* 사이드바 스타일 */
    .sidebar .sidebar-content {
        background-color: #f5f5f5;
    }
    
    /* 푸터 스타일 */
    .footer {
        text-align: center;
        color: #666;
        font-size: 12px;
        margin-top: 30px;
        padding-top: 10px;
        border-top: 1px solid #eee;
    }
    
    /* 애니메이션 스타일 */
    @keyframes pulse {
        0% { opacity: 1; }
        50% { opacity: 0.7; }
        100% { opacity: 1; }
    }
    
    .live-indicator {
        display: inline-block;
        width: 10px;
        height: 10px;
        background-color: #4CAF50;
        border-radius: 50%;
        margin-right: 8px;
        animation: pulse 2s infinite;
    }
    
    /* 비행기 아이콘 애니메이션 */
    @keyframes fly {
        0% { transform: translateX(0) rotate(0deg); }
        100% { transform: translateX(20px) rotate(10deg); }
    }
    
    .airplane-icon {
        display: inline-block;
        animation: fly 2s infinite alternate;
    }
    
    /* 버튼 스타일 */
    .stButton button {
        background-color: #0a4d8c;
        color: white;
        border-radius: 20px;
        padding: 8px 16px;
        font-weight: bold;
        border: none;
        transition: all 0.3s;
    }
    
    .stButton button:hover {
        background-color: #1976d2;
        transform: translateY(-2px);
        box-shadow: 0 4px 8px rgba(0, 0, 0, 0.2);
    }
</style>
""", unsafe_allow_html=True)

# 헤더 섹션
st.markdown("""
<div class="title-container">
    <h1>
        <span class="airplane-icon">✈️</span> 
        인천국제공항 실시간 정보 시스템
    </h1>
    <p>실시간 입국장 혼잡도 및 항공편 정보를 시각적으로 확인하세요</p>
</div>
""", unsafe_allow_html=True)

# API 키 설정
API_KEY = "4q1sVXi0cPESZlljpKfTU7CxdXYfGycZKuBakPEOYWMHS4h8VaetyuTMI89MS12gmh2jd1uiBrkEzKc%2FzqVg4w%3D%3D"
BASE_URL = "http://apis.data.go.kr/B551177/StatusOfArrivals/getArrivalsCongestion"

# API 데이터 가져오기
@st.cache_data(ttl=60)  # 1분마다 데이터 갱신
def fetch_data(terminal, num_rows=100, page_no=1, response_type="json", airport=None):
    params = {
        "serviceKey": API_KEY,
        "numOfRows": num_rows,
        "pageNo": page_no,
        "terno": terminal,
        "type": response_type
    }
    
    if airport:
        params["airport"] = airport
    
    try:
        response = requests.get(BASE_URL, params=params)
        
        if response_type == "json":
            data = response.json()
            if 'response' in data and 'body' in data['response'] and 'items' in data['response']['body']:
                items = data['response']['body']['items']
                if isinstance(items, dict) and 'item' in items:
                    if isinstance(items['item'], list):
                        return pd.DataFrame(items['item'])
                    else:
                        return pd.DataFrame([items['item']])
            return pd.DataFrame()
        else:  # XML 처리
            root = ET.fromstring(response.content)
            items = []
            for item in root.findall('.//item'):
                item_dict = {child.tag: child.text for child in item}
                items.append(item_dict)
            return pd.DataFrame(items)
    except Exception as e:
        st.error(f"데이터를 가져오는 중 오류가 발생했습니다: {e}")
        return pd.DataFrame()
