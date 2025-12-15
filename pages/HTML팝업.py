import streamlit as st
import folium
from streamlit_folium import st_folium

st.title("📸 사진과 정보가 뜨는 팝업")

# 1. 기본 지도 생성
m = folium.Map(location=[35.8714, 128.6014], zoom_start=13)

# 2. 팝업에 들어갈 HTML 코드 작성
# 파이썬의 f-string을 쓰면 변수를 넣기 편합니다.
# 실제로는 DB에서 가져온 데이터나 이미지 URL을 넣으면 됩니다.

# 예시: 현장 사진 (인터넷 이미지)과 점검표
html_code = """
<div style="font-family: malgun gothic; width: 300px;">
    <h4 style="margin-bottom:10px;">🚧 1공구 가스 배관 점검</h4>
    
    <img src="https://via.placeholder.com/300x150?text=Site+Photo" style="width:100%; border-radius:10px; margin-bottom:10px;">
    
    <table style="width:100%; border-collapse: collapse; border: 1px solid #ddd;">
        <tr style="background-color: #f2f2f2;">
            <th style="border: 1px solid #ddd; padding: 8px;">항목</th>
            <th style="border: 1px solid #ddd; padding: 8px;">결과</th>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">가스 압력</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: blue;"><b>정상 (2.3kPa)</b></td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">누출 여부</td>
            <td style="border: 1px solid #ddd; padding: 8px; color: green;">없음</td>
        </tr>
        <tr>
            <td style="border: 1px solid #ddd; padding: 8px;">담당자</td>
            <td style="border: 1px solid #ddd; padding: 8px;">백경호</td>
        </tr>
    </table>
    
    <p style="margin-top:10px; font-size:12px; color:gray;">점검일시: 2025-12-12 14:00</p>
    
    <a href="https://www.daesungenergy.com" target="_blank" 
       style="display:block; text-align:center; background-color:#008CBA; color:white; padding:10px; text-decoration:none; border-radius:5px;">
       상세 보고서 보기
    </a>
</div>
"""

# 3. IFrame을 사용하여 팝업 크기 고정
# HTML 내용이 많을 때는 IFrame을 쓰는 게 레이아웃 깨짐 방지에 좋습니다.
iframe = folium.IFrame(html_code, width=320, height=350)
popup = folium.Popup(iframe, max_width=320)

# 4. 마커에 팝업 추가
folium.Marker(
    location=[35.8714, 128.6014],
    popup=popup,
    icon=folium.Icon(color='blue', icon='info-sign')
).add_to(m)

st.info("지도 중앙의 마커를 클릭해보세요! 사진과 표가 나옵니다.")

# 5. 지도 표시
st_folium(m, width=700, height=500)