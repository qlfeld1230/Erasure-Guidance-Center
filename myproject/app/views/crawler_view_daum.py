import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# 카카오 API 필요
'''
daum crawler
다음에서 각각의 요소로 검색을 수행함
'''


def daum_crawler(user_data, headers, search_limit):
    # user_data로부터 정보를 참조
    name = user_data["get_name"]()
    nickname = user_data["get_nickname"]()
    affiliation = user_data["get_affiliation"]()
    email = user_data["get_email"]()

    # 각 검색어 쿼리로 설정
    search_query_name = name
    search_query_nickname = nickname
    search_query_affiliation = affiliation
    search_query_email = email

    # 크롤링 결과를 저장할 리스트
    daum_link_list = []

    # 검색에 사용될 쿼리
    daum_url_name = f"https://search.daum.net/search?w=web&q={requests.utils.quote(search_query_name)}"
    daum_url_nickname = f"https://search.daum.net/search?w=web&q={requests.utils.quote(search_query_nickname)}"
    daum_url_affiliation = f"https://search.daum.net/search?w=web&q={requests.utils.quote(search_query_affiliation)}"
    daum_url_email = f"https://search.daum.net/search?w=web&q={requests.utils.quote(search_query_email)}"

    # 다음 크롤링 for name
    daum_response_name = requests.get(daum_url_name, headers=headers)
    if daum_response_name.status_code == 200:
        daum_soup_name = BeautifulSoup(daum_response_name.text, 'html.parser')
        items_name = daum_soup_name.select('a.f_link_b')  # 적합한 CSS 선택자 수정 필요
        for item in items_name:
            link_text = item.get_text()
            link_url = item.get('href')
            if name in link_text:
                daum_link_list.append({'text': link_text, 'url': link_url})
            if len(daum_link_list) >= search_limit:
                break

    # 다음 크롤링 for nickname
    daum_response_nickname = requests.get(daum_url_nickname, headers=headers)
    if daum_response_nickname.status_code == 200:
        daum_soup_nickname = BeautifulSoup(
            daum_response_nickname.text, 'html.parser')
        items_nickname = daum_soup_nickname.select('a.f_link_b')
        for item in items_nickname:
            link_text = item.get_text()
            link_url = item.get('href')
            if nickname in link_text:
                daum_link_list.append({'text': link_text, 'url': link_url})
            if len(daum_link_list) >= search_limit:
                break

    # 다음 크롤링 for affiliation
    daum_response_affiliation = requests.get(
        daum_url_affiliation, headers=headers)
    if daum_response_affiliation.status_code == 200:
        daum_soup_affiliation = BeautifulSoup(
            daum_response_affiliation.text, 'html.parser')
        items_affiliation = daum_soup_affiliation.select('a.f_link_b')
        for item in items_affiliation:
            link_text = item.get_text()
            link_url = item.get('href')
            if affiliation in link_text:
                daum_link_list.append({'text': link_text, 'url': link_url})
            if len(daum_link_list) >= search_limit:
                break

    # 다음 크롤링 for email
    daum_response_email = requests.get(daum_url_email, headers=headers)
    if daum_response_email.status_code == 200:
        daum_soup_email = BeautifulSoup(
            daum_response_email.text, 'html.parser')
        items_email = daum_soup_email.select('a.f_link_b')
        for item in items_email:
            link_text = item.get_text()
            link_url = item.get('href')
            if email in link_text:
                daum_link_list.append({'text': link_text, 'url': link_url})
            if len(daum_link_list) >= search_limit:
                break

    # 검색 결과 개수 계산
    daum_result_count = len(daum_link_list)

    return daum_link_list, daum_result_count
