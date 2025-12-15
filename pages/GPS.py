import streamlit as st
import folium
from folium.plugins import LocateControl
from streamlit_folium import st_folium

st.title("📡 내 위치 찾기 (GPS)")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. GPS 버튼 추가 (LocateControl)
LocateControl(
    auto_start=False,           # True면 지도 로딩되자마자 위치 찾기 시도
    position='topleft',         # 버튼 위치
    strings={
        "title": "내 위치 보기", # 마우스 올렸을 때 툴팁
        "popup": "현재 위치"     # 위치 찾은 후 뜨는 팝업
    },
    locateOptions={
        "enableHighAccuracy": True # 고정밀 모드 (모바일에서 배터리 더 씀)
    }
).add_to(m)

st.info("지도 왼쪽 상단의 📍 아이콘을 누르면 브라우저가 위치 권한을 요청합니다. '허용'을 눌러주세요.")

# 3. 지도 표시
st_folium(m, width=700, height=500)