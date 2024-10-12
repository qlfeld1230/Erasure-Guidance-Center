import requests
from bs4 import BeautifulSoup
from django.shortcuts import render

def crawler_view(request):
    # 크롤링할 URL 설정
    url = "https://google.com"  # 원하는 웹사이트로 변경 가능

    # 웹 페이지 요청 보내기
    response = requests.get(url)
    
    # 응답 코드 확인
    if response.status_code != 200:
        return render(request, 'error.html', {'message': '크롤링 실패: ' + str(response.status_code)})

    # HTML 파싱
    soup = BeautifulSoup(response.text, 'html.parser')

    # 제목 추출
    page_title = soup.title.string

    # 모든 링크 추출
    links = soup.find_all('a')
    link_list = [{'text': link.get_text(), 'url': link.get('href')} for link in links if link.get('href')]

    # 결과를 템플릿으로 전달
    return render(request, 'crawler.html', {
        'page_title': page_title,
        'link_list': link_list,
    })
