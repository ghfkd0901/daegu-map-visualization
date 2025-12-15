import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import time

st.title("🏎️ 실시간 이동 궤적 (TripsLayer)")

# 1. 데이터 생성 (수정됨: 좌표와 시간을 분리)
@st.cache_data
def generate_path_data():
    data = []
    center_lat, center_lon = 35.8714, 128.6014
    
    for i in range(50):
        path_coords = [] # 좌표만 담을 리스트 [x, y]
        timestamps = []  # 시간만 담을 리스트 [t]
        
        start_lon = center_lon + np.random.uniform(-0.05, 0.05)
        start_lat = center_lat + np.random.uniform(-0.05, 0.05)
        
        d_lon = np.random.uniform(-0.002, 0.002)
        d_lat = np.random.uniform(-0.002, 0.002)
        
        for t in range(100):
            lon = start_lon + (d_lon * t) + np.random.normal(0, 0.0001)
            lat = start_lat + (d_lat * t) + np.random.normal(0, 0.0001)
            
            path_coords.append([lon, lat]) # 좌표 추가
            timestamps.append(t)           # 시간 추가
            
        data.append({
            "path": path_coords,
            "timestamps": timestamps
        })
        
    return data

df = pd.DataFrame(generate_path_data())

# 2. 지도 초기 설정
view_state = pdk.ViewState(
    latitude=35.8714,
    longitude=128.6014,
    zoom=11,
    pitch=45,
    bearing=0
)

# 3. 레이어 설정 함수 (수정됨: 단순 컬럼명 사용)
def get_deck(current_time):
    layer = pdk.Layer(
        "TripsLayer",
        df,
        get_path="path",            # 이제 'path' 컬럼엔 좌표만 있습니다.
        get_timestamps="timestamps",# 'timestamps' 컬럼을 바로 가져옵니다. (JS 코드 불필요)
        get_color=[255, 255, 0],
        opacity=0.8,
        width_min_pixels=5,
        rounded=True,
        trail_length=30,
        current_time=current_time
    )
    
    return pdk.Deck(
        layers=[layer],
        initial_view_state=view_state,
        map_style='mapbox://styles/mapbox/dark-v10',
        tooltip=False
    )

# 4. 애니메이션 실행
st.info("👇 아래 버튼을 누르면 10초간 이동 흐름이 재생됩니다.")
start_btn = st.button("▶️ 애니메이션 시작")

chart_placeholder = st.empty()

if start_btn:
    for t in range(0, 100, 2):
        deck = get_deck(t)
        chart_placeholder.pydeck_chart(deck)
        time.sleep(0.05)
    st.success("재생 완료!")
else:
    chart_placeholder.pydeck_chart(get_deck(50))