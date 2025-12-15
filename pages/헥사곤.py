import streamlit as st
import pydeck as pdk
import pandas as pd
import numpy as np
import geopandas as gpd
import os

st.set_page_config(page_title="3D 헥사곤 맵", layout="wide")
st.title("⬢ 대구광역시 3D 헥사곤 밀도 맵 (높이 수정)")
st.caption("지도를 드래그해서 돌려보세요! 데이터가 밀집된 곳일수록 기둥이 높고 색이 진해집니다.")

# 1. 데이터 로드 (대구 구역 가져오기 - 범위 제한용)
@st.cache_data
def load_data_hex():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shp_path = os.path.join(current_dir, '..', '지도', '국가기본도_시군구구역경계', 'TN_SIGNGU_BNDRY.shp')
    
    if not os.path.exists(shp_path): return None
    
    gdf = gpd.read_file(shp_path, encoding='cp949')
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    daegu_gdf = daegu_gdf.to_crs(epsg=4326) # 위경도 변환
    return daegu_gdf

# 2. 가상 데이터 포인트 생성
def generate_hex_data(gdf, total_points=2000):
    data = []
    for _, row in gdf.iterrows():
        center = row.geometry.centroid
        n_points = np.random.randint(50, 300)
        latitudes = np.random.normal(center.y, 0.02, n_points)
        longitudes = np.random.normal(center.x, 0.02, n_points)
        
        for lat, lon in zip(latitudes, longitudes):
            # PyDeck은 [Longitude(경도), Latitude(위도)] 순서
            data.append([float(lon), float(lat)])
            
    return pd.DataFrame(data, columns=['lon', 'lat'])

gdf = load_data_hex()
if gdf is None: st.stop()

# 데이터 생성 (Session State로 고정)
if 'hex_data' not in st.session_state:
    st.session_state['hex_data'] = generate_hex_data(gdf)

df = st.session_state['hex_data']

# 3. 헥사곤 레이어 설정
layer = pdk.Layer(
    "HexagonLayer",
    df,
    get_position=["lon", "lat"],
    radius=200,             # 육각형 하나의 반지름 (미터 단위)
    # ----------------------------------------------------------
    # [수정] elevation_scale 값을 줄여서 기둥 높이를 낮춤
    # ----------------------------------------------------------
    elevation_scale=10,     # 기존 50 -> 10으로 변경 (5배 낮춤)
    elevation_range=[0, 3000], # 데이터 값에 따른 높이 매핑 범위
    pickable=True,
    extruded=True,          # 3D 돌출 여부
    coverage=1,
    auto_highlight=True,
)

# 4. 뷰 설정 (대구 중심, 45도 기울임)
view_state = pdk.ViewState(
    longitude=128.6014,
    latitude=35.8714,
    zoom=10,
    min_zoom=5,
    max_zoom=15,
    pitch=40.5, # 기울기
    bearing=-27.36, # 회전
)

# 5. 렌더링
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={
        "html": "<b>밀집도:</b> {elevationValue}개 포인트",
        "style": {"color": "white"}
    },
    map_style='mapbox://styles/mapbox/dark-v10'
)

st.pydeck_chart(r)

st.divider()
st.info("💡 **Tip:** `elevation_scale` 값을 조절하여 기둥의 전체적인 높이를 변경할 수 있습니다.")