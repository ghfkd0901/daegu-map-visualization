import streamlit as st
import folium
from folium.plugins import AntPath
from streamlit_folium import st_folium
import numpy as np # 곡선 계산을 위해 필요

st.set_page_config(page_title="항공 경로 시각화(곡선)", layout="wide")
st.title("✈️ 대구국제공항 항공 네트워크 (Curved Path)")
st.caption("베지에 곡선(Bezier Curve)을 적용하여 실제 항공로처럼 부드러운 곡선을 표현합니다.")

# 1. 좌표 데이터
daegu_airport = [35.894, 128.614]

destinations = {
    "제주(CJU)": [33.5104, 126.4913],
    "인천(ICN)": [37.4602, 126.4407],
    "도쿄(NRT)": [35.7720, 140.3929],
    "방콕(BKK)": [13.6900, 100.7501],
    "타이베이(TPE)": [25.0797, 121.2342],
    "다낭(DAD)": [16.0544, 108.2022],
    "싱가포르(SIN)": [1.3644, 103.9915], # 적도 근처라 곡선이 예쁘게 나옴
    "블라디보스토크(VVO)": [43.1300, 131.9000]
}

# -----------------------------------------------------------------------------
# [핵심] 베지에 곡선 생성 함수 (직선을 곡선으로 바꿔주는 마법)
# -----------------------------------------------------------------------------
def get_bezier_curve(p1, p2, num_points=100):
    # p1: 시작점 [lat, lon], p2: 끝점 [lat, lon]
    start = np.array(p1)
    end = np.array(p2)
    
    # 1. 두 점 사이의 거리 계산 (거리가 멀수록 곡선을 더 높게 띄우기 위함)
    dist = np.linalg.norm(start - end)
    
    # 2. 제어점(Control Point) 생성 - 곡선의 '허리'를 꺾을 지점
    # 중점에서 위도(lat)를 살짝 올려서 아치형을 만듦
    midpoint = (start + end) / 2
    
    # 거리에 비례해서 곡률(Curvature) 조정 (0.2는 곡 휘어짐 정도)
    # 3D 지구본 느낌을 내기 위해 위도(x축) 방향으로 오프셋을 줌
    control_point = midpoint + np.array([dist * 0.3, 0]) 

    # 3. 베지에 공식 적용 (t는 0부터 1까지 흐르는 시간)
    points = []
    for t in np.linspace(0, 1, num_points):
        # 2차 베지에 곡선 공식: B(t) = (1-t)^2 * P0 + 2(1-t)t * P1 + t^2 * P2
        point = (1 - t)**2 * start + 2 * (1 - t) * t * control_point + t**2 * end
        points.append(point.tolist())
        
    return points
# -----------------------------------------------------------------------------

# 지도 생성
m = folium.Map(location=[30, 128], zoom_start=5, tiles='CartoDB dark_matter')

# 대구공항 마커
folium.Marker(
    daegu_airport,
    popup="<b>대구국제공항 (TAE)</b>",
    icon=folium.Icon(color='red', icon='plane', prefix='fa')
).add_to(m)

# 경로 그리기
for name, dest_coord in destinations.items():
    # 목적지 마커
    folium.Marker(
        dest_coord,
        popup=f"<b>{name}</b>",
        icon=folium.Icon(color='blue', icon='info-sign')
    ).add_to(m)
    
    # [변경] 직선 대신 '곡선 좌표 리스트'를 생성해서 넣음
    curved_path = get_bezier_curve(daegu_airport, dest_coord)
    
    AntPath(
        locations=curved_path, # 곡선 좌표 입력
        dash_array=[10, 20],
        delay=800,
        color='cyan',    # 형광색
        pulse_color='white',
        weight=2,
        opacity=0.8,
        hardware_acceleration=True # 부드러운 애니메이션
    ).add_to(m)

st.sidebar.header("✈️ 운항 노선 (곡선 적용)")
st.sidebar.info("직선보다 실제 항공로에 가까운 아치형 경로입니다.")

st_folium(m, use_container_width=True)