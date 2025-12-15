import streamlit as st
import geopandas as gpd
import pydeck as pdk
import os
import numpy as np

# 1. 페이지 설정
st.set_page_config(page_title="대구 3D 지도(Fix)", layout="wide")
st.title("🏙️ 대구광역시 3D 입체 지도 (수정버전)")
st.caption("Shift 키 + 마우스 드래그로 지도를 회전/기울이기 해보세요!")

# 2. 데이터 로드
@st.cache_data
def load_data_3d():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shp_path = os.path.join(current_dir, '..', '지도', '국가기본도_시군구구역경계', 'TN_SIGNGU_BNDRY.shp')
    
    if not os.path.exists(shp_path): return None
    
    gdf = gpd.read_file(shp_path, encoding='cp949')
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    
    # Dissolve
    daegu_gdf = daegu_gdf.dissolve(by='ADZONE_NM', as_index=False).reset_index(drop=True)
    
    # 좌표계 변환 (위경도)
    if daegu_gdf.crs is None: daegu_gdf.set_crs("EPSG:5179", inplace=True)
    daegu_gdf = daegu_gdf.to_crs(epsg=4326)

    # [가상 데이터] 높이(Elevation) 데이터 생성
    # 높이 차이가 확 나도록 100 ~ 2000 사이로 설정
    daegu_gdf['elevation'] = np.random.randint(100, 2000, size=len(daegu_gdf))
    
    # [색상] R, G, B 리스트로 변환 (PyDeck 필수!)
    # 여기서는 값을 기준으로 파란색~보라색 계열로 만듦
    daegu_gdf['fill_color'] = daegu_gdf['elevation'].apply(
        lambda x: [
            int(x/2000 * 255),  # R (높을수록 붉은 기)
            0,                  # G
            255 - int(x/2000 * 100), # B
            200                 # A (투명도)
        ]
    )
    
    return daegu_gdf

df = load_data_3d()

if df is None:
    st.error("데이터 파일이 없습니다.")
    st.stop()

# 3. PyDeck 설정 (GeoJsonLayer 사용)
# 초기 뷰 설정 (대구)
view_state = pdk.ViewState(
    latitude=35.8714,
    longitude=128.6014,
    zoom=10,
    pitch=50, # 50도 기울임 (입체감)
    bearing=30 # 30도 회전
)

# [핵심 변경] PolygonLayer -> GeoJsonLayer
# GeoJsonLayer가 GeoPandas 데이터를 훨씬 더 잘 받아먹습니다.
layer = pdk.Layer(
    "GeoJsonLayer",
    df,
    pickable=True,                 # 마우스 올리면 정보 뜨게
    stroked=True,                  # 테두리 그리기
    filled=True,                   # 색 채우기
    extruded=True,                 # [중요] 3D 돌출 효과 켜기
    wireframe=True,                # 와이어프레임(선) 보이기
    get_elevation="elevation",     # 높이 컬럼 지정
    elevation_scale=5,             # 높이 배율 (너무 높으면 줄이고, 낮으면 키우세요)
    get_fill_color="fill_color",   # 색상 컬럼 지정
    get_line_color=[255, 255, 255],# 테두리 흰색
    get_line_width=20
)

# 4. 렌더링 (지도 스타일 변경: 기본 스타일 사용)
# map_style을 None으로 하면 기본 지도가 나옵니다. (에러 방지용)
r = pdk.Deck(
    layers=[layer],
    initial_view_state=view_state,
    tooltip={"text": "{ADZONE_NM}\n높이: {elevation}"},
    map_style=None # 맵박스 키 없이도 안전하게 렌더링
)

st.pydeck_chart(r)