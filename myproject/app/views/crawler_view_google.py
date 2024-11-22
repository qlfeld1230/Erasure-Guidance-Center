import requests
from bs4 import BeautifulSoup
from django.shortcuts import render


def google_crawler(user_data, headers, search_limit):
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
    google_link_list = []

    # 검색에 사용될 쿼리
    google_url_name = f"https://www.google.com/search?q={requests.utils.quote(search_query_name)}"
    google_url_nickname = f"https://www.google.com/search?q={requests.utils.quote(search_query_nickname)}"
    google_url_affiliation = f"https://www.google.com/search?q={requests.utils.quote(search_query_affiliation)}"
    google_url_email = f"https://www.google.com/search?q={requests.utils.quote(search_query_email)}"

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
    google_result_count = len(google_link_list)

    return google_link_list, google_result_count
