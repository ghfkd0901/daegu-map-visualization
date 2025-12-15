import streamlit as st
import geopandas as gpd
import folium
from folium.plugins import TimestampedGeoJson
from streamlit_folium import st_folium
import os
import numpy as np
import pandas as pd
from datetime import datetime, timedelta

st.set_page_config(page_title="설치 이력 타임랩스", layout="wide")
st.title("⏱️ 연소기 설치 이력 타임랩스 (데이터 고정)")
st.caption("Session State를 적용하여 재생 중 데이터가 바뀌지 않습니다.")

# 1. 데이터 로드 (기본 지도 모양)
@st.cache_data
def load_base_map():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shp_path = os.path.join(current_dir, '..', '지도', '국가기본도_시군구구역경계', 'TN_SIGNGU_BNDRY.shp')
    
    if not os.path.exists(shp_path): return None
    
    gdf = gpd.read_file(shp_path, encoding='cp949')
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    
    # 구역 합치기
    daegu_gdf = daegu_gdf.dissolve(by='ADZONE_NM', as_index=False).reset_index(drop=True)

    # Timestamp 에러 방지 (문자열 변환)
    for col in daegu_gdf.columns:
        if col != 'geometry':
            daegu_gdf[col] = daegu_gdf[col].astype(str)

    if daegu_gdf.crs is None: daegu_gdf.set_crs("EPSG:5179", inplace=True)
    daegu_gdf = daegu_gdf.to_crs(epsg=4326)
    
    return daegu_gdf

# 2. 시계열(Time-Series) 가상 데이터 생성
def generate_time_data(gdf, count=300):
    features = []
    start_date = datetime(2024, 1, 1)
    
    for _ in range(count):
        # 1. 랜덤 위치 선정
        random_district = gdf.sample(1).iloc[0].geometry
        minx, miny, maxx, maxy = random_district.bounds
        while True:
            pnt = pd.DataFrame({'x': [np.random.uniform(minx, maxx)], 'y': [np.random.uniform(miny, maxy)]})
            pnt_gdf = gpd.GeoDataFrame(pnt, geometry=gpd.points_from_xy(pnt.x, pnt.y))
            pnt_gdf.set_crs(epsg=4326, inplace=True)
            
            if random_district.contains(pnt_gdf.iloc[0].geometry):
                point = pnt_gdf.iloc[0].geometry
                break
        
        # 2. 랜덤 날짜 생성
        random_days = np.random.randint(0, 365)
        event_date = start_date + timedelta(days=random_days)
        date_str = event_date.strftime("%Y-%m-%d")
        
        # 3. GeoJSON Feature 구조 생성
        feature = {
            'type': 'Feature',
            'geometry': {
                'type': 'Point',
                'coordinates': [point.x, point.y],
            },
            'properties': {
                'time': date_str,
                'style': {'color': 'blue'},
                'icon': 'circle',
                'iconstyle': {
                    'fillColor': 'blue',
                    'fillOpacity': 0.6,
                    'stroke': 'false',
                    'radius': 5
                },
                'popup': f"설치일: {date_str}"
            }
        }
        features.append(feature)
    return features

daegu_gdf = load_base_map()

if daegu_gdf is None: 
    st.error("데이터 파일을 찾을 수 없습니다.")
    st.stop()

# -----------------------------------------------------------------------------
# [핵심] Session State로 타임랩스 데이터 고정하기
# -----------------------------------------------------------------------------
if 'time_features' not in st.session_state:
    with st.spinner("⏳ 초기 타임랩스 데이터를 생성 중입니다..."):
        st.session_state['time_features'] = generate_time_data(daegu_gdf)

# 새로고침 버튼 (데이터 다시 뽑고 싶을 때)
if st.button("🔄 데이터 재생성"):
    with st.spinner("⏳ 새로운 데이터를 생성 중입니다..."):
        st.session_state['time_features'] = generate_time_data(daegu_gdf)
    st.rerun()

# 저장된 데이터 사용
time_features = st.session_state['time_features']
# -----------------------------------------------------------------------------

# 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=11)

# 배경 지도 추가
folium.GeoJson(
    daegu_gdf,
    style_function=lambda x: {'color': 'gray', 'fillOpacity': 0.1, 'weight': 1}
).add_to(m)

# TimestampedGeoJson 추가
TimestampedGeoJson(
    {'type': 'FeatureCollection', 'features': time_features},
    period='P1D',
    duration='P7D',
    add_last_point=True,
    auto_play=False,
    loop=False,
    max_speed=1,
    loop_button=True,
    date_options='YYYY/MM/DD',
    time_slider_drag_update=True
).add_to(m)

# 지도 출력 (returned_objects=[] 로 리로드 방지)
st_folium(m, use_container_width=True, returned_objects=[])