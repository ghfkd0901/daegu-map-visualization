import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium

st.title("⚡ 움직이는 배관 흐름 (AntPath)")

# 1. 기본 지도 생성 (대구 중심)
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 경로 데이터 (위도, 경도 리스트)
# 실제로는 파이프라인 좌표 데이터를 리스트로 넣으면 됩니다.
# 예시: 대구 시청 -> 동대구역 방향 가상의 경로
path_coordinates = [
    [35.8714, 128.6014], # 시작점
    [35.8720, 128.6050],
    [35.8740, 128.6100],
    [35.8760, 128.6150],
    [35.8770, 128.6200],
    [35.8780, 128.6280]  # 끝점
]

# 3. AntPath 설정 및 추가
AntPath(
    locations=path_coordinates,
    delay=1000,          # 애니메이션 속도 (숫자가 클수록 느림)
    weight=6,            # 선 두께
    color='blue',        # 배경 선 색상
    pulse_color='white', # 움직이는 점선 색상 (흐름)
    opacity=0.7,         # 투명도
    reverse=False,       # 흐름 방향 반대로 할지 여부
    tooltip="메인 공급관 A라인"
).add_to(m)

# 4. 시작/끝 지점 마커 (선택사항)
folium.Marker(path_coordinates[0], popup="공급 시작").add_to(m)
folium.Marker(path_coordinates[-1], popup="공급 끝", icon=folium.Icon(color='red')).add_to(m)

# 5. 지도 표시
st_folium(m, width=700)