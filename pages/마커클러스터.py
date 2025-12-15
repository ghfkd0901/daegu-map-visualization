import streamlit as st
import folium
from folium.plugins import MarkerCluster
from streamlit_folium import st_folium
import pandas as pd
import numpy as np

st.title("🗺️ 고정된 데이터 지도 (캐싱 적용)")

# 1. 데이터 생성 함수 (캐싱 적용)
# @st.cache_data가 붙으면 이 함수는 입력값이 바뀌지 않는 한
# 결과를 메모리에 저장해두고 재사용합니다.
@st.cache_data
def load_data():
    # 실제 업무에서는 여기서 DB 쿼리나 크롤링을 수행합니다.
    df = pd.DataFrame({
        'lat': np.random.uniform(35.84, 35.90, 50),
        'lon': np.random.uniform(128.55, 128.65, 50),
        'title': [f'현장 {i}' for i in range(50)],
        'category': np.random.choice(['안전', '공사', '민원'], 50) # 예시 카테고리 추가
    })
    return df

# 데이터 로드 (이제 새로고침해도 데이터가 변하지 않습니다)
data = load_data()

# 2. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=12)

# 3. 마커 클러스터 생성
marker_cluster = MarkerCluster().add_to(m)

# 4. 마커 추가
for i, row in data.iterrows():
    # 카테고리별 아이콘 색상 구분 (간단한 예시)
    icon_color = 'red' if row['category'] == '안전' else 'blue'
    
    folium.Marker(
        location=[row['lat'], row['lon']],
        popup=f"<b>{row['category']}</b><br>{row['title']}",
        tooltip=row['title'],
        icon=folium.Icon(color=icon_color, icon='info-sign')
    ).add_to(marker_cluster)

# 5. 지도 표시
st_folium(m, width=700)