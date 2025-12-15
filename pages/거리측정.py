import streamlit as st
import folium
from folium.plugins import MeasureControl
from streamlit_folium import st_folium

st.title("📏 거리 및 면적 측정 도구")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 측정 도구 추가
# position: 도구 위치 (topright, topleft, bottomright, bottomleft)
# primary_length_unit: 거리 측정 기본 단위 (meters, kilometers, miles 등)
measure_control = MeasureControl(
    position='topright',
    primary_length_unit='meters', 
    secondary_length_unit='kilometers',
    primary_area_unit='sqmeters', # 면적 단위 (평은 없어서 m²로 계산 후 변환 필요)
    active_color='orange',        # 측정 중일 때 선 색상
    completed_color='red'         # 측정 완료 후 선 색상
)
m.add_child(measure_control)

st.info("지도 우측 상단의 📐 아이콘을 클릭하고, 지도 위에 점을 찍어보세요. 더블 클릭하면 측정이 끝납니다.")

# 3. 지도 표시
st_folium(m, width=700)