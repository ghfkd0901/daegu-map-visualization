import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os
import numpy as np 

# 1. 페이지 설정
st.set_page_config(page_title="대구 보급률 시각화(POC)", layout="wide")

st.title("💧 대구광역시 구별 가스 보급률 현황 (POC)")
st.caption("이 지도는 0% ~ 100% 사이의 가상 보급률 데이터를 시각화한 예시입니다.")

# 2. 데이터 로드 및 가상 데이터 생성 함수
@st.cache_data
def load_data_rate():
    # -----------------------------------------------------------
    # 경로 설정 (pages 폴더 기준)
    # -----------------------------------------------------------
    current_dir = os.path.dirname(os.path.abspath(__file__))
    shp_path = os.path.join(current_dir, '..', '지도', '국가기본도_시군구구역경계', 'TN_SIGNGU_BNDRY.shp')
    
    if not os.path.exists(shp_path):
        return None
    
    # 데이터 읽기
    gdf = gpd.read_file(shp_path, encoding='cp949')
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    
    # Dissolve (구역 합치기)
    daegu_gdf = daegu_gdf.dissolve(by='ADZONE_NM', as_index=False)
    daegu_gdf = daegu_gdf.reset_index(drop=True)

    # 에러 방지용 문자 변환
    for col in daegu_gdf.columns:
        if col != 'geometry':
            daegu_gdf[col] = daegu_gdf[col].astype(str)
            
    # 좌표계 변환
    if daegu_gdf.crs is None:
        daegu_gdf.set_crs("EPSG:5179", inplace=True)
    daegu_gdf = daegu_gdf.to_crs(epsg=4326)
    
    # -----------------------------------------------------------
    # [NEW] 보급률(%) 가상 데이터 생성
    # -----------------------------------------------------------
    # 60.0% ~ 98.0% 사이의 실수(float) 랜덤 생성
    dummy_rates = np.random.uniform(60.0, 98.0, size=len(daegu_gdf))
    
    # 깔끔하게 소수점 1자리에서 반올림
    daegu_gdf['보급률'] = np.round(dummy_rates, 1)
    
    return daegu_gdf

# 3. 메인 실행 로직
daegu_gdf = load_data_rate()

if daegu_gdf is None:
    st.error("데이터 파일을 찾을 수 없습니다.")
    st.stop()

# 사이드바 정보
st.sidebar.header("📊 보급률 통계 (가상)")
st.sidebar.metric("평균 보급률", f"{daegu_gdf['보급률'].mean():.1f}%")
st.sidebar.write("가장 높은 곳:", daegu_gdf.loc[daegu_gdf['보급률'].idxmax(), 'ADZONE_NM'])
st.sidebar.write("가장 낮은 곳:", daegu_gdf.loc[daegu_gdf['보급률'].idxmin(), 'ADZONE_NM'])

# 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=10)

folium.Choropleth(
    geo_data=daegu_gdf,
    data=daegu_gdf,
    columns=['ADZONE_NM', '보급률'],
    key_on='feature.properties.ADZONE_NM',
    fill_color='PuBu',     # [변경] Purple-Blue 색상 (보급률 느낌)
    fill_opacity=0.8,      # 색을 좀 더 진하게
    line_opacity=0.2,
    legend_name='보급률 (%)',
    highlight=True
).add_to(m)

# 툴팁 추가 (단위 % 붙이기)
folium.GeoJson(
    daegu_gdf,
    style_function=lambda x: {'fillOpacity': 0, 'color': 'transparent'},
    tooltip=folium.GeoJsonTooltip(
        fields=['ADZONE_NM', '보급률'],
        aliases=['지역명:', '보급률:'],
        localize=True
    )
).add_to(m)

st_folium(m, use_container_width=True)

# 하단 표
st.divider()
st.subheader("📋 구별 보급률 순위")
# 보급률 높은 순서대로 정렬해서 보여줌
st.dataframe(
    daegu_gdf[['ADZONE_NM', '보급률']].sort_values(by='보급률', ascending=False),
    use_container_width=True
)