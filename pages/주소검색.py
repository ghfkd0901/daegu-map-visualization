import streamlit as st
import folium
from folium.plugins import Geocoder
from streamlit_folium import st_folium

st.title("🔍 주소 및 장소 검색")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 지오코더(검색창) 추가
# add_marker=True: 검색한 위치에 자동으로 마커를 찍어줍니다.
geocoder = Geocoder(
    position='topleft', 
    add_marker=True,
    collapsed=False  # True로 하면 돋보기 아이콘만 보이고, 클릭해야 검색창이 열립니다.
)
m.add_child(geocoder)

# 3. 설명 추가
st.info("지도 왼쪽 상단 검색창에 'Daegu' 또는 'Daesung Energy' 처럼 영어/한글로 장소를 검색해보세요.")

# 4. 지도 표시
st_folium(m, width=700, height=500)