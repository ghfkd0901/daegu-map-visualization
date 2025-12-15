import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
import numpy as np 

# 1. 페이지 설정
st.set_page_config(page_title="대구 연소기 현황(POC)", layout="wide")

st.title("🔥 대구광역시 구별 취사용 연소기 현황 (POC)")
st.caption("이 지도는 가상의 임의 데이터를 사용한 시각화 예시입니다.")

# 2. 데이터 로드 및 가상 데이터 생성 함수
@st.cache_data
def load_data_with_dummy():
    # -----------------------------------------------------------
    # [핵심 변경] 경로를 안전하게 잡는 법 (os.path 사용)
    # -----------------------------------------------------------
    # 1. 현재 이 파일(취사용.py)의 절대 경로를 찾음 (.../02_지도시각화/pages)
    current_dir = os.path.dirname(os.path.abspath(__file__))
    
    # 2. 부모 폴더(..)로 올라가서 '지도' 폴더로 연결
    # 결과: .../02_지도시각화/지도/국가기본도.../TN_SIGNGU_BNDRY.shp
    shp_path = os.path.join(current_dir, '..', '지도', '국가기본도_시군구구역경계', 'TN_SIGNGU_BNDRY.shp')
    
    # 경로가 진짜 맞는지 확인 (디버깅용, 나중에 지워도 됨)
    if not os.path.exists(shp_path):
        st.error(f"❌ 파일을 못 찾았어요! 경로 확인: {shp_path}")
        return None
    
    # 데이터 읽기
    gdf = gpd.read_file(shp_path, encoding='cp949')
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    
    # Dissolve: 구역 합치기
    daegu_gdf = daegu_gdf.dissolve(by='ADZONE_NM', as_index=False)
    daegu_gdf = daegu_gdf.reset_index(drop=True)

    # 날짜/텍스트 형식 문자열 변환
    for col in daegu_gdf.columns:
        if col != 'geometry':
            daegu_gdf[col] = daegu_gdf[col].astype(str)
            
    # 좌표계 변환
    if daegu_gdf.crs is None:
        daegu_gdf.set_crs("EPSG:5179", inplace=True)
    daegu_gdf = daegu_gdf.to_crs(epsg=4326)
    
    # -----------------------------------------------------------
    # 가상 데이터 생성
    # -----------------------------------------------------------
    dummy_counts = np.random.randint(5000, 50001, size=len(daegu_gdf))
    daegu_gdf['연소기_수'] = dummy_counts
    
    return daegu_gdf

# 3. 메인 실행 로직
daegu_gdf = load_data_with_dummy()

if daegu_gdf is None:
    st.stop() # 데이터 없으면 여기서 멈춤

# 사이드바 정보
st.sidebar.header("POC 데이터 정보")
st.sidebar.success("가상 데이터 생성 완료")
st.sidebar.metric("평균 연소기 수 (가상)", f"{int(daegu_gdf['연소기_수'].mean()):,}개")

# 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=10)

folium.Choropleth(
    geo_data=daegu_gdf,
    data=daegu_gdf,
    columns=['ADZONE_NM', '연소기_수'],
    key_on='feature.properties.ADZONE_NM',
    fill_color='YlOrRd',
    fill_opacity=0.7,
    line_opacity=0.2,
    legend_name='취사용 연소기 수 (가상 데이터)',
    bins=5,
    highlight=True
).add_to(m)

# 툴팁 추가
folium.GeoJson(
    daegu_gdf,
    style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'},
    tooltip=folium.GeoJsonTooltip(
        fields=['ADZONE_NM', '연소기_수'],
        aliases=['지역명:', '연소기 수(가상):'],
        localize=True
    )
).add_to(m)

st_folium(m, use_container_width=True)

st.divider()
st.subheader("📊 생성된 가상 데이터 확인")
st.dataframe(daegu_gdf[['ADZONE_NM', '연소기_수']].sort_values(by='연소기_수', ascending=False))