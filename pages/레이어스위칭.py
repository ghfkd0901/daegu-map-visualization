import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🎛️ 레이어 껐다 켜기 (Layer Control)")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 그룹(Layer) 생성
# 현장 유형별로 그룹을 만듭니다. name에 들어가는 텍스트가 체크박스 이름이 됩니다.
fg_construction = folium.FeatureGroup(name="🚧 공사 현장")
fg_safety = folium.FeatureGroup(name="⚠️ 안전 점검")
fg_office = folium.FeatureGroup(name="🏢 지사 위치")

# 3. 마커를 각 그룹에 추가 (m.add_to가 아니라 fg.add_to 사용)

# [공사 현장 그룹]
folium.Marker(
    [35.875, 128.605], popup="1공구 현장", 
    icon=folium.Icon(color='blue', icon='wrench')
).add_to(fg_construction)

folium.Marker(
    [35.865, 128.610], popup="2공구 현장", 
    icon=folium.Icon(color='blue', icon='wrench')
).add_to(fg_construction)

# [안전 점검 그룹]
folium.Marker(
    [35.870, 128.595], popup="가스 누출 의심", 
    icon=folium.Icon(color='red', icon='warning-sign')
).add_to(fg_safety)

# [지사 위치 그룹] - 서클 마커 사용
folium.CircleMarker(
    [35.8714, 128.6014], radius=10, color='green', fill=True, popup="대구 지사"
).add_to(fg_office)


# 4. 그룹을 지도에 등록
fg_construction.add_to(m)
fg_safety.add_to(m)
fg_office.add_to(m)

# 5. 레이어 컨트롤 추가 (가장 마지막에!)
# collapsed=False: 메뉴가 펼쳐진 상태로 시작
folium.LayerControl(collapsed=False).add_to(m)

# 6. 지도 표시
st_folium(m, width=700)