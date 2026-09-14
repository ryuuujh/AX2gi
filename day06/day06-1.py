# folium으로 지도에 마커를 표시하는 예제 코드
# import folium
# 도쿄 시내 명소 4곳의 좌표(위도/경도)와 이름을 리스트로 받아 folium 지도를 만들고
# 각 좌표에 이름표가 붙은 마커를 찍은다음, basic_map.html 파일로 저장하고
# 저장된 basicmap.html 파일을 웹 브라우저로 열어서 확인하는 코드 생성
# 이건 streamlit이 아니기 때문에 python day06-1.py 로 실행

# 도쿄 시내 명소 4곳 이름, 위도, 경도 샘플데이터

# 지도의 시작 중심 좌표 (도쿄타워 기준) 지정해서 folium 지도 객체 생성
# 숫자가 클수록 더 가깝게 보여준다

# 리스트에 담긴 장소들을 하나씩 꺼내며 지도위 마커를 추가하는 코드 생성

"""도쿄 명소 지도를 저장하고 브라우저로 열기: python day06-1.py"""

from pathlib import Path
import webbrowser

import folium

# 도쿄 시내 명소 4곳 이름, 위도, 경도 샘플데이터
places = [
    ("시부야스카이", 35.6584, 139.7022),
    ("도쿄타워", 35.6586, 139.7454),
    ("JR신주쿠역", 35.6909, 139.7003),
    ("아사쿠사 센소지", 35.7148, 139.7967),
]


def main():
    # 도쿄타워를 중심으로 지도를 생성한다. 확대 수준은 숫자가 클수록 가깝다.
    tokyo_tower = [35.6586, 139.7454]
    tokyo_map = folium.Map(location=tokyo_tower, zoom_start=13)

    # 마우스를 올리거나 클릭하면 장소 이름이 나타난다.
    for name, latitude, longitude in places:
        folium.Marker(
            location=[latitude, longitude],
            tooltip=name,
            popup=folium.Popup(name, max_width=250),
        ).add_to(tokyo_map)

    # 실행 위치와 관계없이 파이썬 파일과 같은 폴더에 저장한다.
    output_path = Path(__file__).resolve().with_name("basic_map.html")
    tokyo_map.save(str(output_path))
    print(f"지도 저장 완료: {output_path}")

    if not webbrowser.open(output_path.as_uri()):
        print("브라우저를 자동으로 열지 못했습니다. 저장된 HTML 파일을 직접 열어주세요.")


if __name__ == "__main__":
    main()