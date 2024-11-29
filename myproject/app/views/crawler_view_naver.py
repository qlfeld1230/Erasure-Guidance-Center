import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

'''
naver crewler
네이버에서 각각의 요소로 검색을 수행함
'''


def naver_crawler(user_data, headers, search_limit):
    # crewler_view.py의 user data 참조

    queries = {
        "name": user_data["get_name"](),
        "nickname": user_data["get_nickname"](),
        "affiliation": user_data["get_affiliation"](),
        "email": user_data["get_email"](),
        "birth": user_data["get_birth"](),
        "phone": user_data["get_phone"](),
    }

    # 검색에 사용될 쿼리
    naver_urls = {
        key: f"https://search.naver.com/search.naver?query={requests.utils.quote(value)}"
        for key, value in queries.items()
        if value  # 값이 None이나 빈 문자열이 아닌 경우에만 포함
    }

    # 크롤링 결과를 저장할 리스트
    naver_link_list = []

    for key, url in naver_urls.items():
        naver_response = requests.get(url, headers=headers)
        if naver_response.status_code == 200:
            naver_soup = BeautifulSoup(naver_response.text, 'html.parser')
            items = naver_soup.select('a.api_txt_lines')
            for item in items:
                link_text = item.get_text()  # 제목
                link_url = item.get('href')  # URL
                description_element = item.find_next('div')  # 본문 내용 추출 (추정)
                description = description_element.get_text() if description_element else "내용 없음"

                # 제목 길이 제한: 20자 초과 시 자르고 "..." 추가
                if len(link_text) > 50:
                    link_text = link_text[:50] + "..."
                # 본문 내용 길이 제한: 50자 초과 시 자르고 "..." 추가
                if len(description) > 300:
                    description = description[:300] + "..."

                naver_link_list.append(
                    {'text': link_text, 'url': link_url, 'description': description})
                if len(naver_link_list) >= search_limit:
                    break

    # 검색 결과 개수 계산
    naver_result_count = len(naver_link_list)

    return naver_link_list, naver_result_count
