import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np

st.title("🌈 3D 입체 연결망 (Pydeck ArcLayer)")

# 1. 데이터 준비 (매우 중요!)
# ArcLayer는 '시작점 위경도'와 '도착점 위경도' 4개의 컬럼이 필요합니다.

# 중심점 (예: 대구 시청 부근)
center_lat, center_lon = 35.8714, 128.6014

data = []
# 중심점에서 주변으로 뻗어나가는 30개의 가상 경로 생성
for i in range(30):
    # 랜덤한 도착점 생성 (중심 주변 반경 약 5~10km 내)
    target_lat = center_lat + np.random.uniform(-0.07, 0.07)
    target_lon = center_lon + np.random.uniform(-0.08, 0.08)
    
    # [시작 경도, 시작 위도, 도착 경도, 도착 위도] 순서로 저장
    data.append([center_lon, center_lat, target_lon, target_lat])

df = pd.DataFrame(data, columns=["src_lon", "src_lat", "tgt_lon", "tgt_lat"])


# 2. Pydeck 시각화 설정

# 2-1. 초기 시점 (View State) 설정
# 3D를 제대로 느끼려면 지도를 기울여야(pitch) 합니다.
view_state = pdk.ViewState(
    latitude=center_lat,
    longitude=center_lon,
    zoom=11,
    pitch=50,    # 지도 기울기 (0~60도). 높을수록 3D 느낌.
    bearing=30   # 지도 회전 각도 (동서남북 방향)
)

# 2-2. 아치 레이어 (ArcLayer) 정의
arc_layer = pdk.Layer(
    "ArcLayer",
    data=df,
    get_source_position=["src_lon", "src_lat"], # 시작점 컬럼 지정
    get_target_position=["tgt_lon", "tgt_lat"], # 도착점 컬럼 지정
    get_source_color=[0, 255, 128, 200],        # 시작점 색상 (RGBA: 민트색)
    get_target_color=[255, 0, 0, 200],          # 도착점 색상 (RGBA: 빨간색)
    get_width=4,                                # 선 두께
    get_tilt=15,                                # 아치의 기울어짐 정도 (역동감 추가)
    pickable=True,                              # 마우스 오버 시 반응 여부
    auto_highlight=True,                        # 마우스 오버 시 하이라이트
)

# 3. Deck 객체 생성 및 Streamlit에 표시
# map_style='mapbox://styles/mapbox/dark-v10' 등 다른 스타일도 가능하지만,
# 기본 스타일(None)이 가장 무난합니다.
# 3. Deck 객체 생성 및 Streamlit에 표시
deck = pdk.Deck(
    layers=[arc_layer],
    initial_view_state=view_state,  # 여기가 수정되었습니다! (view_style -> view_state)
    tooltip={"text": "경로 연결"}
)

st.pydeck_chart(deck)

st.info("💡 **Tip:** 지도 위에서 마우스 왼쪽 버튼을 누른 채 드래그하면 이동, **Ctrl(또는 Cmd) + 왼쪽 클릭 드래그**하면 지도를 **회전 및 기울이기** 할 수 있습니다!")