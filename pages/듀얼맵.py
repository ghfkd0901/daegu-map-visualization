import streamlit as st
import folium
from folium.plugins import DualMap
from streamlit_folium import st_folium

st.title("⚖️ 비교 분석용 DualMap")

# 1. DualMap 생성
# layout='vertical'로 하면 위아래로 나뉩니다. 기본은 좌우(horizontal).
m = DualMap(location=[35.8714, 128.6014], zoom_start=14, layout='horizontal')

# 2. 왼쪽 지도 (m.m1) 설정 - 일반 지도 느낌
# 타일 레이어를 명시적으로 설정
folium.TileLayer('OpenStreetMap').add_to(m.m1)
folium.Marker(
    [35.8714, 128.6014], 
    popup="<b>계획 노선</b>", 
    icon=folium.Icon(color='blue', icon='cloud')
).add_to(m.m1)

# 3. 오른쪽 지도 (m.m2) 설정 - 다른 테마 (예: CartoDB)
# 위성 지도를 쓰고 싶다면 타일 URL을 넣어야 하는데, 여기선 테마가 다른 지도로 예시를 듭니다.
folium.TileLayer('CartoDB positron').add_to(m.m2)
folium.Marker(
    [35.8714, 128.6014], 
    popup="<b>실제 시공</b>", 
    icon=folium.Icon(color='red', icon='info-sign')
).add_to(m.m2)

# 4. Streamlit에 표시
# DualMap은 HTML 구조가 좀 달라서 st_folium보다는 static HTML로 뿌리는 게 안전할 때가 많습니다.
# 하지만 st_folium도 최신 버전에서는 지원하니 시도해봅니다.
st_folium(m, width=900, height=500)