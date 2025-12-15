import streamlit as st
import folium
from folium.plugins import SideBySideLayers
from streamlit_folium import st_folium

st.title("↔️ 스와이프 맵 (Side By Side)")

# 1. 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=14)

# 2. 두 개의 서로 다른 레이어 생성
# 왼쪽: 일반 지도 (OpenStreetMap)
layer_left = folium.TileLayer('OpenStreetMap', name='일반 지도')
# 오른쪽: 위성 느낌 지도 (CartoDB Positron - 예시용)
# 실제로는 'Google Satellite' 같은 타일이나, 다른 연도의 데이터를 씁니다.
layer_right = folium.TileLayer('CartoDB dark_matter', name='다크 모드')

layer_left.add_to(m)
layer_right.add_to(m)

# 3. 스와이프 컨트롤 추가
# layer_left와 layer_right를 슬라이더로 구분합니다.
sbs = SideBySideLayers(layer_left=layer_left, layer_right=layer_right)
m.add_child(sbs)

st.info("지도 중앙에 있는 수직 바(Slider)를 좌우로 움직여보세요!")
st_folium(m, width=700, height=500)