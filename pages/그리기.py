import streamlit as st
import folium
from folium.plugins import Draw
from streamlit_folium import st_folium

st.title("🖍️ 지도 위에 그리기 (Draw Tool)")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 그리기 도구 추가
# export=True: 그린 내용을 GeoJSON 파일로 다운로드할 수 있는 버튼이 생깁니다.
draw = Draw(
    export=True,
    position='topleft',
    draw_options={
        'polyline': True,  # 선 그리기
        'polygon': True,   # 다각형(구역) 그리기
        'circle': True,    # 원 그리기
        'rectangle': True, # 사각형 그리기
        'marker': True,    # 마커 찍기
        'circlemarker': False,
    },
    edit_options={'edit': True} # 그린 도형 수정 가능 여부
)
draw.add_to(m)

# 3. 지도 표시 및 데이터 가져오기
# 사용자가 그림을 그리면 그 결과가 'output' 변수에 담깁니다.
output = st_folium(m, width=700, height=500)

# 4. 그린 데이터 확인하기 (좌표 추출)
st.subheader("💾 그린 영역의 좌표 데이터")

if output.get("all_drawings"):
    # 사용자가 그린 모든 도형의 정보가 여기 들어있습니다.
    drawings = output["all_drawings"]
    
    # 가장 최근에 그린 도형 정보만 보기
    if output.get("last_active_drawing"):
        last_draw = output["last_active_drawing"]
        geometry_type = last_draw['geometry']['type']
        coords = last_draw['geometry']['coordinates']
        
        st.success(f"방금 그린 도형: **{geometry_type}**")
        st.code(f"좌표 정보: {coords}")
        
        # 실제 활용 팁: 
        # 이 좌표(coords)를 DB에 저장하면 '공사 구역'이나 '순찰 경로'를 기록할 수 있습니다.
else:
    st.info("지도 왼쪽 상단의 도구 모음을 눌러서 그림을 그려보세요!")