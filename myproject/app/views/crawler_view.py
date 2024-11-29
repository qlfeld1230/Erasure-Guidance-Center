import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import random

from .crawler_view_naver import naver_crawler
from .crawler_view_google import google_crawler

'''
IP 차단 회피를 방지하기 위한
agent 로테이션
'''


def get_random_user_agent():
    user_agents = [
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0",
        "Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/90.0.4430.93 Safari/537.36",
        "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Safari/605.1.15",
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Edge/91.0.864.59",
    ]
    return random.choice(user_agents)


'''
user data 공간
'''


def user_data():
    return {
        "get_name": lambda: "권호열",
        "get_nickname": lambda: "hykwon",
        "get_affiliation": lambda: "강원대학교",
        "get_email": lambda: "hykwon@kangwon.ac.kr",
        "get_birth": lambda: "720503",
        "get_phone": lambda: "033-250-6383",
    }


'''
검색어 강조 처리 함수
'''


def highlight_results(results, search_keyword):
    """
    검색어를 강조하여 반환합니다.
    여러 검색어를 처리하도록 수정.
    """
    if not search_keyword:
        return results

    highlighted_results = []
    for result in results:
        # 제목과 설명에서 검색어 강조 처리
        highlighted_text = result['text']
        highlighted_description = result['description']

        # 검색어 강조
        highlighted_text = highlighted_text.replace(
            search_keyword, f"<mark>{search_keyword}</mark>"
        )
        highlighted_description = highlighted_description.replace(
            search_keyword, f"<mark>{search_keyword}</mark>"
        )

        highlighted_results.append({
            'text': highlighted_text,
            'url': result['url'],
            'description': highlighted_description,
        })

    return highlighted_results


def integrated_crawler_view(request):
    # 사용자 데이터 생성
    user = user_data()

    # 검색어 조합 (사용자 정보 기반)
    search_keywords = [
        user["get_name"](),
        user["get_email"](),
        user["get_affiliation"](),
        user["get_birth"](),
        user["get_phone"](),
    ]

    # 검색 키워드 출력 (디버깅)
    print("검색 키워드:", search_keywords)

    # 크롤링 차단 우회를 위한 헤더 설정
    headers = {"User-Agent": get_random_user_agent()}

    # 검색결과 수 제한
    search_limit = 20

    # 네이버 크롤러 호출
    naver_link_list, naver_result_count = naver_crawler(
        user, headers, search_limit)

    # 구글 크롤러 호출
    google_link_list, google_result_count = google_crawler(
        user, headers, search_limit)

    # 검색 키워드 강조 처리
    for keyword in search_keywords:
        naver_link_list = highlight_results(naver_link_list, keyword)
        google_link_list = highlight_results(google_link_list, keyword)

    # 결과를 템플릿으로 전달
    return render(request, 'crawler.html', {
        'page_title': '통합 검색 결과',
        'naver_link_list': naver_link_list,
        'google_link_list': google_link_list,
        'naver_result_count': naver_result_count,
        'google_result_count': google_result_count,
        'search_query': ', '.join(search_keywords),  # 사용된 검색 키워드
    })
