import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
import time
import random


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
    '''
    이름
    별명
    소속
    주민번호
    이메일

    '''
    name = ""
    nickname = ""
    affiliation = ""
    id_national = ""
    email = ""

    # (Getter, Setter)

    # Name

    def get_name():
        return name

    def set_name(new_name):
        nonlocal name  # 외부 변수 name에 접근하기 위해 nonlocal 사용
        name = new_name

    # NickName
    def get_nickname():
        return nickname

    def set_nickname(new_nickname):
        nonlocal nickname
        nickname = new_nickname

    # National ID
    def get_id_national():
        return id_national

    def set_id_national(new_id_national):
        nonlocal id_national
        id_national = new_id_national

    # Email
    def get_email():
        return email

    def set_email(new_email):
        nonlocal email
        email = new_email

    # affiliation
    def get_affiliation():
        return affiliation

    def set_affiliation(new_affiliation):
        nonlocal affiliation
        affiliation = new_affiliation

    # 함수들을 딕셔너리로 반환하여 외부에서 접근 가능하게 하기
    return {
        "get_name": get_name,
        "set_name": set_name,
        "get_nickname": get_nickname,
        "set_nickname": set_nickname,
        "get_id_national": get_id_national,
        "set_id_national": set_id_national,
        "get_email": get_email,
        "set_email": set_email,
        "get_affiliation": get_affiliation,
        "set_affiliation": set_affiliation,
    }


def integrated_crawler_view(request):
    if request.method == "POST":
        # 검색어 입력값 가져오기
        search_query = request.POST.get('query')

        # _____________________수정한 것___________________
        user = user_data()

        # 추후 DB 연동
        user["set_name"]("박성호")
        user["set_nickname"]("곰두리")
        user["set_affiliation"]("강원대학교")
        user["set_email"]("qlfeld1230@naver.com")

        # 데이터 가져오기

        name = user["get_name"]()
        nickname = user["get_nickname"]()
        affiliation = user["get_affiliation"]()
        email = user["get_email"]()

       # OR 조건으로 이름과 별명 각각 검색
        search_query_name = name
        search_query_nickname = nickname
        search_query_affiliation = affiliation
        search_query_email = email

        # 검색결과 수 제한
        search_limit = 20

        # 크롤링 차단 우회를 위한 헤더 설정
        headers = {
            "User-Agent": get_random_user_agent()
        }

        naver_link_list = []

        naver_url_name = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_name)}"
        naver_url_nickname = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_nickname)}"
        naver_url_affiliation = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_affiliation)}"
        naver_url_email = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_email)}"

        google_link_list = []

        google_url_name = f"https://www.google.com/search?q={requests.utils.quote(search_query_name)}"
        google_url_nickname = f"https://www.google.com/search?q={requests.utils.quote(search_query_nickname)}"
        google_url_affiliation = f"https://www.google.com/search?q={requests.utils.quote(search_query_affiliation)}"
        google_url_email = f"https://www.google.com/search?q={requests.utils.quote(search_query_email)}"

        # 네이버 크롤링 for name
        naver_response_name = requests.get(naver_url_name, headers=headers)
        if naver_response_name.status_code == 200:
            naver_soup_name = BeautifulSoup(
                naver_response_name.text, 'html.parser')
            items_name = naver_soup_name.select('a.api_txt_lines')
            for item in items_name:
                link_text = item.get_text()
                link_url = item.get('href')
                if name in link_text:
                    naver_link_list.append(
                        {'text': link_text, 'url': link_url})
                if len(naver_link_list) >= search_limit:
                    break

        # 네이버 크롤링 for nickname
        naver_response_nickname = requests.get(
            naver_url_nickname, headers=headers)
        if naver_response_nickname.status_code == 200:
            naver_soup_nickname = BeautifulSoup(
                naver_response_nickname.text, 'html.parser')
            items_nickname = naver_soup_nickname.select('a.api_txt_lines')
            for item in items_nickname:
                link_text = item.get_text()
                link_url = item.get('href')
                if nickname in link_text:
                    naver_link_list.append(
                        {'text': link_text, 'url': link_url})
                if len(naver_link_list) >= search_limit:
                    break

        # 네이버 크롤링 for affiliation
        naver_response_affiliation = requests.get(
            naver_url_affiliation, headers=headers)
        if naver_response_affiliation.status_code == 200:
            naver_soup_affiliation = BeautifulSoup(
                naver_response_affiliation.text, 'html.parser')
            items_affiliation = naver_soup_affiliation.select(
                'a.api_txt_lines')
            for item in items_affiliation:
                link_text = item.get_text()
                link_url = item.get('href')
                if affiliation in link_text:
                    naver_link_list.append(
                        {'text': link_text, 'url': link_url})
                if len(naver_link_list) >= search_limit:
                    break

        # 네이버 크롤링 for email
        naver_response_email = requests.get(naver_url_email, headers=headers)
        if naver_response_email.status_code == 200:
            naver_soup_email = BeautifulSoup(
                naver_response_email.text, 'html.parser')
            items_email = naver_soup_email.select('a.api_txt_lines')
            for item in items_email:
                link_text = item.get_text()
                link_url = item.get('href')
                if email in link_text:
                    naver_link_list.append(
                        {'text': link_text, 'url': link_url})
                if len(naver_link_list) >= search_limit:
                    break

        # 구글 크롤링 for name
        google_response_name = requests.get(google_url_name, headers=headers)

        if google_response_name.status_code == 200:
            google_soup_name = BeautifulSoup(
                google_response_name.text, 'html.parser')

            results_name = google_soup_name.select('div.MjjYud')
            for result in results_name:
                # 제목 추출
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""

                # 링크 추출
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'

                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""
                if name in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description})
                if len(google_link_list) >= search_limit:
                    break

        # 구글 크롤링 for nickname
        google_response_nickname = requests.get(
            google_url_nickname, headers=headers)
        if google_response_nickname.status_code == 200:
            google_soup_nickname = BeautifulSoup(
                google_response_nickname.text, 'html.parser')
            results_nickname = google_soup_nickname.select('div.MjjYud')
            for result in results_nickname:
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""
                if nickname in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description})
                if len(google_link_list) >= search_limit:
                    break

        # 구글 크롤링 for affiliation
        google_response_affiliation = requests.get(
            google_url_affiliation, headers=headers)
        if google_response_affiliation.status_code == 200:
            google_soup_affiliation = BeautifulSoup(
                google_response_affiliation.text, 'html.parser')
            results_affiliation = google_soup_affiliation.select('div.MjjYud')
            for result in results_affiliation:
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""
                if affiliation in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description})
                if len(google_link_list) >= search_limit:
                    break

        # 구글 크롤링 for email
        google_response_email = requests.get(google_url_email, headers=headers)
        if google_response_email.status_code == 200:
            google_soup_email = BeautifulSoup(
                google_response_email.text, 'html.parser')
            results_email = google_soup_email.select('div.MjjYud')
            for result in results_email:
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""
                if email in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description})
                if len(google_link_list) >= search_limit:
                    break

        # 검색 결과 개수 계산
        naver_result_count = len(naver_link_list)
        google_result_count = len(google_link_list)

        # 결과를 템플릿으로 전달
        return render(request, 'crawlernew.html', {
            'page_title': '통합 검색 결과',
            'naver_link_list': naver_link_list,
            'google_link_list': google_link_list,
            'naver_result_count': naver_result_count,
            'google_result_count': google_result_count,
            'search_query': search_query,
        })

        # # 결과를 템플릿으로 전달
        # return render(request, 'crawler.html', {
        #     'page_title': '통합 검색 결과',
        #     'naver_link_list': naver_link_list,
        #     'google_link_list': google_link_list,
        #     'search_query': search_query,
        # })

    # GET 요청일 경우 기본 페이지 렌더링
    return render(request, 'crawlernew.html')
