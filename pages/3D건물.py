import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

st.title("🏙️ 디지털 트윈: 구역별 입체 시각화")

# 1. 데이터 생성 (가상의 건물/구역 데이터)
# 중심점: 대구
center_lat, center_lon = 35.8714, 128.6014

data = []
# 50개의 가상 구역 생성
for i in range(50):
    # 구역 중심 랜덤 생성
    lon = center_lon + np.random.uniform(-0.02, 0.02)
    lat = center_lat + np.random.uniform(-0.02, 0.02)
    
    # 가스 사용량 (높이로 쓸 값)
    usage = np.random.randint(10, 500)
    
    # 사각형 폴리곤 좌표 생성 (작은 구역)
    # 실제로는 행정구역이나 건물 경계 좌표를 넣습니다.
    d = 0.001 # 구역 크기
    polygon = [
        [lon - d, lat - d],
        [lon + d, lat - d],
        [lon + d, lat + d],
        [lon - d, lat + d],
        [lon - d, lat - d] # 다시 시작점으로 닫아줌
    ]
    
    data.append({
        "coordinates": polygon,
        "usage": usage,
        "name": f"구역-{i+1}"
    })

df = pd.DataFrame(data)

# 2. Pydeck 시각화 설정

# 2-1. 초기 시점 (3D 느낌 나게 기울이기)
view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=13,
    pitch=45, 
    bearing=0
)

# 2-2. 폴리곤 레이어 설정
polygon_layer = pdk.Layer(
    "PolygonLayer",
    df,
    get_polygon="coordinates",
    get_fill_color="[255, 255 - (usage / 2), 0, 200]", # 사용량이 높을수록 붉은색, 낮을수록 노란색
    get_elevation="usage",       # 'usage' 컬럼 값만큼 높이를 올림
    elevation_scale=5,           # 높이 배율 (데이터 값이 작으면 키워줌)
    extruded=True,               # True여야 입체적으로 튀어나옴 (False면 그냥 바닥에 색칠)
    pickable=True,               # 마우스 오버 가능
    auto_highlight=True,         # 마우스 오버 시 반짝임
)

# 3. 렌더링
deck = pdk.Deck(
    layers=[polygon_layer],
    initial_view_state=view_state,
    tooltip={"text": "{name}\n사용량: {usage}"},
    map_style='mapbox://styles/mapbox/light-v9' # 깔끔한 밝은 지도
)

st.pydeck_chart(deck)

st.caption("건물의 높이와 색상은 '가스 사용량' 데이터를 기반으로 합니다. (노랑=낮음, 빨강=높음)")