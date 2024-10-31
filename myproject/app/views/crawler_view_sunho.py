import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

# user data 공간


def user_data():

    name = ""
    nickname = ""
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

        # 데이터 가져오기

        name = user["get_name"]()
        nickname = user["get_nickname"]()

       # OR 조건으로 이름과 별명 각각 검색
        search_query_name = name
        search_query_nickname = nickname

        naver_link_list = []

        # 검색결과 수 제한
        search_limit = 20

        # 네이버 크롤링 for name
        naver_url_name = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_name)}"
        naver_response_name = requests.get(naver_url_name)
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
                if len(naver_link_list) >= 10:
                    break

        # 네이버 크롤링 for nickname
        naver_url_nickname = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query_nickname)}"
        naver_response_nickname = requests.get(naver_url_nickname)
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
                if len(naver_link_list) >= 10:
                    break

        google_link_list = []
        google_url_name = f"https://www.google.com/search?q={requests.utils.quote(search_query_name)}"
        google_url_nickname = f"https://www.google.com/search?q={requests.utils.quote(search_query_nickname)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }

        # 구글 크롤링 for name
        google_response_name = requests.get(google_url_name, headers=headers)
        if google_response_name.status_code == 200:
            google_soup_name = BeautifulSoup(
                google_response_name.text, 'html.parser')
            results_name = google_soup_name.select('div.MjjYud')
            for result in results_name:
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""
                if name in (title + description):
                    google_link_list.append(
                        {'text': title, 'url': link, 'description': description})
                if len(google_link_list) >= 10:
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
                if len(google_link_list) >= 10:
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
