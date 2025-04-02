# 데이터 전처리 함수
def preprocess_data(df):
    if df.empty:
        return df
    
    # 데이터 타입 변환
    if 'foreigner' in df.columns:
        df['foreigner'] = pd.to_numeric(df['foreigner'], errors='coerce').fillna(0)
    if 'korean' in df.columns:
        df['korean'] = pd.to_numeric(df['korean'], errors='coerce').fillna(0)
    
    # 날짜 변환
    if 'estimatedtime' in df.columns:
        df['estimatedtime'] = pd.to_datetime(df['estimatedtime'], format='%Y%m%d%H%M', errors='coerce')
    if 'scheduletime' in df.columns:
        df['scheduletime'] = pd.to_datetime(df['scheduletime'], format='%Y%m%d%H%M', errors='coerce')
    
    # 총 인원 계산
    if 'foreigner' in df.columns and 'korean' in df.columns:
        df['total_people'] = df['foreigner'] + df['korean']
    
    return df

# 혼잡도 수준 계산 함수
def get_congestion_level(count):
    if count < 50:
        return "여유", "#4CAF50"  # 녹색
    elif count < 100:
        return "보통", "#FFC107"  # 노란색
    else:
        return "혼잡", "#F44336"  # 빨간색