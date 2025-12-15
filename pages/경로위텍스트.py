import streamlit as st
import folium
from folium.plugins import PolyLineTextPath
from streamlit_folium import st_folium

st.title("〰️ 배관 따라 글자 쓰기 (Text Path)")

m = folium.Map(location=[35.8714, 128.6014], zoom_start=14)

# 1. 꼬불꼬불한 경로 데이터 (예: 가스 배관)
path_coords = [
    [35.8714, 128.6014],
    [35.8730, 128.6050],
    [35.8720, 128.6100],
    [35.8750, 128.6150],
    [35.8740, 128.6200]
]

# 2. 기본 선 그리기
polyline = folium.PolyLine(path_coords, color="blue", weight=5).add_to(m)

# 3. 선 위에 텍스트 입히기
# repeat=True: 선이 길면 글자를 반복해서 찍음
# offset: 선에서 얼마나 떨어져서 글자를 쓸지 (중앙은 0)
PolyLineTextPath(
    polyline,
    "       >> 대성 가스 공급관 (고압) >>       ",
    repeat=True,
    offset=8,
    attributes={'fill': 'blue', 'font-weight': 'bold', 'font-size': '18'}
).add_to(m)

st_folium(m, width=700)