import streamlit as st
import geopandas as gpd
import folium
from streamlit_folium import st_folium
import os

# 1. 페이지 설정
st.set_page_config(page_title="대구 지도 시각화", layout="wide")

st.title("🗺️ 대구광역시 행정구역 시각화")
st.caption("GeoPandas(Dissolve 적용)와 Folium을 활용한 대구 시군구 통합 지도입니다.")

# 2. 데이터 로드 함수
@st.cache_data
def load_data():
    # -----------------------------------------------------------
    # 파일 경로 설정 (main.py 기준)
    # -----------------------------------------------------------
    shp_path = '지도/국가기본도_시군구구역경계/TN_SIGNGU_BNDRY.shp'
    
    # 파일 존재 여부 확인
    if not os.path.exists(shp_path):
        return None
    
    # 데이터 읽기 (인코딩 cp949)
    gdf = gpd.read_file(shp_path, encoding='cp949')
    
    # 대구(27) 필터링
    # 컬럼명: LEGLCD_SE (법정동코드)가 '27'로 시작하는 데이터만 추출
    daegu_gdf = gdf[gdf['LEGLCD_SE'].str.startswith('27')].copy()
    
    # -----------------------------------------------------------
    # [핵심 기능] Dissolve: 흩어진 조각들을 구 이름 기준으로 하나로 합치기
    # -----------------------------------------------------------
    # ADZONE_NM(구 이름)이 같은 것끼리 경계를 녹여서 하나로 만듭니다.
    daegu_gdf = daegu_gdf.dissolve(by='ADZONE_NM', as_index=False)
    
    # 합친 후 인덱스를 0, 1, 2... 순서로 깔끔하게 재정렬 (색상 매핑을 위해 필수)
    daegu_gdf = daegu_gdf.reset_index(drop=True)

    # [에러 방지] 날짜/숫자 형식을 문자로 변환
    # 지도 변환 시 Timestamp 객체가 있으면 에러가 발생하므로 문자열로 변경
    for col in daegu_gdf.columns:
        if col != 'geometry':
            daegu_gdf[col] = daegu_gdf[col].astype(str)
            
    # 좌표계 변환 (UTM-K -> 위경도)
    # 국가기본도 원본 좌표계(EPSG:5179)를 지정하고, 지도용(EPSG:4326)으로 변환
    if daegu_gdf.crs is None:
        daegu_gdf.set_crs("EPSG:5179", inplace=True)
    daegu_gdf = daegu_gdf.to_crs(epsg=4326)
    
    return daegu_gdf

# 3. 메인 실행 로직
daegu_gdf = load_data()

if daegu_gdf is None:
    st.error("❌ 데이터 파일을 찾을 수 없습니다.")
    st.code("현재 경로: 지도/국가기본도_시군구구역경계/TN_SIGNGU_BNDRY.shp")
    st.warning("폴더 구조를 다시 확인해주세요!")
else:
    # -----------------------------------------------------------
    # 사이드바 정보 표시
    # -----------------------------------------------------------
    st.sidebar.header("통계 정보")
    st.sidebar.success("데이터 로드 & 병합 성공!")
    
    # 이제 19개가 아니라 8~9개로 나와야 정상입니다.
    st.sidebar.metric("총 행정구역 수", f"{len(daegu_gdf)}개")
    
    # 구역 이름 목록 표시
    st.sidebar.write("### 포함된 구역:")
    st.sidebar.write(daegu_gdf['ADZONE_NM'].tolist())

    # -----------------------------------------------------------
    # 지도 생성 (Folium)
    # -----------------------------------------------------------
    # 대구 중심 좌표
    m = folium.Map(location=[35.8714, 128.6014], zoom_start=10)

    # 색상 리스트 (구역 개수에 맞춰 알록달록하게)
    colors = [
        '#FF0000', '#FF8C00', '#FFD700', '#008000', '#0000FF', 
        '#4B0082', '#9400D3', '#FF1493', '#00CED1', '#808080'
    ]

    # GeoJson 레이어 추가
    folium.GeoJson(
        daegu_gdf,
        style_function=lambda feature: {
            # feature['id']는 0부터 시작하는 인덱스입니다.
            'fillColor': colors[int(feature['id']) % len(colors)] if str(feature['id']).isdigit() else '#3388ff',
            'color': 'black',       # 테두리 색상
            'weight': 1.5,          # 테두리 두께
            'fillOpacity': 0.6      # 면 투명도
        },
        # 마우스 올렸을 때 뜰 이름 (ADZONE_NM: 행정구역명)
        tooltip=folium.GeoJsonTooltip(fields=['ADZONE_NM'], aliases=['지역명:'])
    ).add_to(m)

    # Streamlit 화면에 지도 출력
    st_folium(m, use_container_width=True)

    # -----------------------------------------------------------
    # 하단 데이터 표 (확인용)
    # -----------------------------------------------------------
    st.divider()
    st.subheader("📊 병합된 데이터 확인")
    st.caption("이제 같은 이름을 가진 구역은 하나로 합쳐져서 보입니다.")
    st.dataframe(daegu_gdf.drop(columns='geometry'))