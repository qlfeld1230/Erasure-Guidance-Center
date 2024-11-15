import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import random

from .crawler_view_naver import naver_crawler
from .crawler_view_google import google_crawler
from .crawler_view_daum import daum_crawler

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


# app/views/user_data_module.py
def user_data():
    return {
        "get_name": lambda: "박성호",
        "get_nickname": lambda: "곰두리",
        "get_affiliation": lambda: "강원대학교",
        "get_email": lambda: "qlfeld1230@naver.com"
    }


def integrated_crawler_view(request):
    if request.method == "POST":
        # 검색어 입력값 가져오기
        search_query = request.POST.get('query')

        # 크롤링 차단 우회를 위한 헤더 설정
        headers = {
            "User-Agent": get_random_user_agent()
        }

        # user_data 생성
        user = user_data()

        # 검색결과 수 제한
        search_limit = 20

        # 네이버 크롤러 호출
        naver_link_list, naver_result_count = naver_crawler(
            user, headers, search_limit)

        # 구글 크롤러 호출
        google_link_list, google_result_count = google_crawler(
            user, headers, search_limit)

        # 다음 크롤러 호출
        daum_link_list, daum_result_count = daum_crawler(
            user, headers, search_limit
        )

        # 결과를 템플릿으로 전달
        return render(request, 'crawler.html', {
            'page_title': '통합 검색 결과',
            'naver_link_list': naver_link_list,
            'google_link_list': google_link_list,
            'daum_link_list': daum_link_list,
            'naver_result_count': naver_result_count,
            'google_result_count': google_result_count,
            'daum_result_count': daum_result_count,
            'search_query': search_query,
        })

    # GET 요청일 경우 기본 페이지 렌더링
    return render(request, 'crawler.html')
