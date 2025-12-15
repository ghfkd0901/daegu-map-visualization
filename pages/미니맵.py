import streamlit as st
import folium
from folium.plugins import MiniMap
from streamlit_folium import st_folium

st.title("🗺️ 미니맵이 달린 지도")

m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 미니맵 추가 (딱 2줄이면 끝)
# toggle_display=True: 미니맵을 접었다 폈다 할 수 있음
minimap = MiniMap(toggle_display=True, position='bottomright')
m.add_child(minimap)

folium.Marker([35.8714, 128.6014], popup="대구 중심").add_to(m)

st_folium(m, width=700)