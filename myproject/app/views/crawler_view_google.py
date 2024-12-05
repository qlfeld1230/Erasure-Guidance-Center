import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


def google_crawler(user_data, headers, search_limit):
    # user_data에서 검색 키워드 추출
    queries = {
         "name": user_data["get_name"](),
        "nickname": user_data["get_nickname"](),
        "affiliation": user_data["get_affiliation"](),
        "email": user_data["get_email"](),
        "birth": user_data["get_birth"](),
        "phone": user_data["get_phone"](),
    }

    # 크롤링 결과를 저장할 리스트
    google_link_list = []

    def crawl_google(query):
        """구글 검색 크롤링 함수"""
        url = f"https://www.google.com/search?q={requests.utils.quote(query)}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            results = soup.select('div.MjjYud')
            for result in results:
                # 제목 추출
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""

                # 링크 추출
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else "링크 없음"

                # 본문 내용 추출
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""

                # 검색 키워드 포함 여부 확인
                if query in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description}
                    )
                # 검색 제한에 도달하면 중단
                if len(google_link_list) >= search_limit:
                    return

    # 각 키워드로 크롤링 수행
    for key, query in queries.items():
        crawl_google(query)

    # 검색 결과 개수 계산
    google_result_count = len(google_link_list)

    return google_link_list, google_result_count
