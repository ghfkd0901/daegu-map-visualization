import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🚩 우리 회사 전용 마커 (Custom Icon)")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 커스텀 아이콘 설정
# 인터넷 상의 이미지 주소(URL)를 넣거나, 
# 로컬 파일 경로(예: "images/company_logo.png")를 넣으면 됩니다.

# 예시 1: 안전모 아이콘 (공사 현장)
icon_url1 = "https://cdn-icons-png.flaticon.com/512/3062/3062319.png"  # 무료 아이콘 예시
icon1 = folium.CustomIcon(
    icon_image=icon_url1,
    icon_size=(50, 50), # 아이콘 크기 (가로, 세로 픽셀)
    icon_anchor=(25, 50) # 아이콘의 어느 부분이 좌표에 찍힐지 설정 (중앙 하단으로 맞춤)
)

# 예시 2: 회사 로고 (본사) - 여기서는 예시로 파이썬 로고 사용
icon_url2 = "https://upload.wikimedia.org/wikipedia/commons/c/c3/Python-logo-notext.svg"
icon2 = folium.CustomIcon(
    icon_image=icon_url2,
    icon_size=(40, 40),
    icon_anchor=(20, 20)
)

# 3. 지도에 마커 추가
folium.Marker(
    location=[35.875, 128.605],
    popup="<b>1공구 작업현장</b>",
    tooltip="공사중",
    icon=icon1
).add_to(m)

folium.Marker(
    location=[35.8714, 128.6014],
    popup="<b>대구 본사</b>",
    tooltip="본사",
    icon=icon2
).add_to(m)

st.info("실제 사용 시에는 `icon_image='logo.png'` 처럼 내 컴퓨터에 있는 파일 이름을 넣으시면 됩니다.")

# 4. 지도 표시
st_folium(m, width=700)