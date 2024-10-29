import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def integrated_crawler_view(request):
    if request.method == "POST":
        # 검색어 입력값 가져오기
        search_query = request.POST.get('query')
        search_terms = search_query.split()  # 띄어쓰기로 검색어 분리

        # 네이버 크롤링
        naver_url = f"https://search.naver.com/search.naver?query={requests.utils.quote(search_query)}"
        naver_response = requests.get(naver_url)
        naver_link_list = []
        if naver_response.status_code == 200:
            naver_soup = BeautifulSoup(naver_response.text, 'html.parser')
            items = naver_soup.select('a.api_txt_lines')
            for item in items:
                link_text = item.get_text()
                link_url = item.get('href')
                if all(term in link_text for term in search_terms):
                    naver_link_list.append({'text': link_text, 'url': link_url})
                if len(naver_link_list) >= 10:
                    break

        # 구글 크롤링
        google_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
        }
        google_response = requests.get(google_url, headers=headers)
        google_link_list = []
        if google_response.status_code == 200:
            google_soup = BeautifulSoup(google_response.text, 'html.parser')
            results = google_soup.select('div.MjjYud')  # <div class="MjjYud"> 요소 선택

            for result in results:
                # 제목과 링크 추출
                title_tag = result.select_one('h3')
                title = title_tag.get_text() if title_tag else ""
                link_tag = title_tag.find_parent('a') if title_tag else None
                link = link_tag['href'] if link_tag else '링크 없음'

                # 설명 텍스트 추출
                description_tag = result.select_one('div.VwiC3b')
                description = description_tag.get_text() if description_tag else ""

                # 검색어 포함 여부 확인
                if all(term in (title + description) for term in search_terms):
                    google_link_list.append({'text': title, 'url': link, 'description': description})

                if len(google_link_list) >= 10:
                    break

        # 결과를 템플릿으로 전달
        return render(request, 'crawler.html', {
            'page_title': '통합 검색 결과',
            'naver_link_list': naver_link_list,
            'google_link_list': google_link_list,
            'search_query': search_query,
        })

    # GET 요청일 경우 기본 페이지 렌더링
    return render(request, 'crawler.html')
