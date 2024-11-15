import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

'''
naver crewler
네이버에서 각각의 요소로 검색을 수행함
'''


def naver_crawler(user_data, headers, search_limit):
    # crewler_view.py의 user data 참조

    name = user_data["get_name"]()
    nickname = user_data["get_nickname"]()
    affiliation = user_data["get_affiliation"]()
    email = user_data["get_email"]()

    # OR 조건으로 이름과 별명 각각 검색
    search_query_name = name
    search_query_nickname = nickname
    search_query_affiliation = affiliation
    search_query_email = email

    # 크롤링 결과를 저장할 리스트
    naver_link_list = []

    # 검색에 사용될 쿼리
    naver_url_name = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_name)}"
    naver_url_nickname = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_nickname)}"
    naver_url_affiliation = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_affiliation)}"
    naver_url_email = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_email)}"

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

    # 검색 결과 개수 계산
    naver_result_count = len(naver_link_list)

    return naver_link_list, naver_result_count
