import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("🗺️ 도면 겹쳐보기 (Image Overlay)")

m = folium.Map(location=[35.8714, 128.6014], zoom_start=15)

# 1. 덮어씌울 이미지 URL (내 컴퓨터 파일도 가능)
# 예시: 기상청 레이더 이미지 같은 느낌의 샘플
image_url = "https://upload.wikimedia.org/wikipedia/commons/f/f6/Eruption_of_Nabro_Volcano_2011.jpg"

# 2. 이미지가 들어갈 영역의 좌표 (남서쪽, 북동쪽)
# 이 좌표 사각형 안에 이미지를 꽉 채워 넣습니다.
# 실제 업무에선 도면의 모서리 좌표 2개를 알면 됩니다.
image_bounds = [[35.8650, 128.5950], [35.8780, 128.6100]]

# 3. 이미지 오버레이 추가
folium.raster_layers.ImageOverlay(
    image=image_url,
    bounds=image_bounds,
    opacity=0.6,    # 투명도 (지도가 비쳐 보여야 하니까)
    interactive=True,
    cross_origin=False,
    zindex=1
).add_to(m)

# 영역 표시용 사각형 (확인용)
folium.Rectangle(image_bounds, color='red', weight=2, fill=False).add_to(m)

st.info("지도 위에 붉은 사각형 안을 보세요. 이미지가 지형에 맞춰 덮여 있습니다.")
st_folium(m, width=700)