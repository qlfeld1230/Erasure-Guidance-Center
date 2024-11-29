import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from itertools import combinations

'''
naver crewler
네이버에서 각각의 요소로 검색을 수행함
'''


def naver_crawler(user_data, headers, search_limit):
    # 검색에 사용할 키워드 추출
    queries = [
        user_data["get_name"](),
        user_data["get_nickname"](),
        user_data["get_affiliation"](),
        user_data["get_email"](),
        user_data["get_birth"](),
        user_data["get_phone"](),
    ]
    # 빈 값 제거
    queries = [query for query in queries if query]

    # 최대 2개 키워드를 조합한 AND 검색어 생성
    and_combinations = [" AND ".join(pair)
                        for pair in combinations(queries, 2)]

    # 단일 키워드로 OR 검색어 생성
    or_queries = queries

    # 크롤링 결과 저장
    naver_link_list = []


    # OR 검색 실행
    for single_query in or_queries:
        url = f"https://search.naver.com/search.naver?query={requests.utils.quote(single_query)}"
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'html.parser')
            items = soup.select('a.api_txt_lines')
            for item in items:
                link_text = item.get_text()  # 제목
                link_url = item.get('href')  # URL
                description_element = item.find_next('div')  # 본문 내용 추출 (추정)
                description = description_element.get_text() if description_element else "내용 없음"

                # 제목 및 본문 내용 길이 제한
                link_text = (
                    link_text[:50] + "...") if len(link_text) > 50 else link_text
                description = (
                    description[:300] + "...") if len(description) > 300 else description

                naver_link_list.append({
                    'text': link_text,
                    'url': link_url,
                    'description': description,
                    'query_type': f"OR ({single_query})"
                })

                if len(naver_link_list) >= search_limit:
                    break

    # 검색 결과 개수 계산
    naver_result_count = len(naver_link_list)

    return naver_link_list, naver_result_count
