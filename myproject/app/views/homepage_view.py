from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from ..forms import CustomUserEnrollForm

''' 개요
- EnrollView 는 회원 가입에 사용하는 컨트롤러(뷰) 입니다.
- MainView 는 메인 페이지에 관련된 뷰를 만들겁니다.
'''

''' 메인 뷰
- main.html 랜더링 해줌 / 특별한 기능은 없음 현재
'''
class MainView(View):
    def get(self, request):
        return render(request, 'homepage_main.html')

''' 회원 가입
- get 및 form 으로 페이지 가져오고
- post 로 회원 가입 로직
- post 성공시 login.html 로 리다이렉트
'''
class EnrollView(View):
    def get(self, request):
        form = CustomUserEnrollForm()
        return render(request, 'homepage_enroll.html', {'form': form})

    def post(self, request):
        form = CustomUserEnrollForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')
        else:
            messages.error(request, '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            return render(request, 'homepage_enroll.html', {'form': form})
        
        
        
import requests
from bs4 import BeautifulSoup
from django.shortcuts import render
from concurrent.futures import ThreadPoolExecutor       # 스레드 사용






''' 개요
- 네이버 크롤러
- 구글 크롤러
- 다음 크롤러 
- 바뀌어야 할 중점?
    - 스레드 사용할 건가
    - 페이지 넘어가는 것들, 즉 1 ~ 99 등 동적 크롤링이 필요한가
'''

def fetch_naver_links(search_query, search_terms):
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
    return naver_link_list

def fetch_google_links(search_query, search_terms):
    google_url = f"https://www.google.com/search?q={requests.utils.quote(search_query)}"
    headers = {
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36"
    }
    google_response = requests.get(google_url, headers=headers)
    google_link_list = []
    if google_response.status_code == 200:
        google_soup = BeautifulSoup(google_response.text, 'html.parser')
        results = google_soup.select('div.MjjYud')
        for result in results:
            title_tag = result.select_one('h3')
            title = title_tag.get_text() if title_tag else ""
            link_tag = title_tag.find_parent('a') if title_tag else None
            link = link_tag['href'] if link_tag else '링크 없음'
            description_tag = result.select_one('div.VwiC3b')
            description = description_tag.get_text() if description_tag else ""
            if all(term in (title + description) for term in search_terms):
                google_link_list.append({'text': title, 'url': link, 'description': description})
            if len(google_link_list) >= 10:
                break
    return google_link_list

def integrated_crawler_view(request):
    if request.method == "POST":
        search_query = request.POST.get('query')
        search_terms = search_query.split()

        # ThreadPoolExecutor를 사용하여 Naver와 Google 크롤링을 병렬로 수행
        with ThreadPoolExecutor() as executor:
            naver_future = executor.submit(fetch_naver_links, search_query, search_terms)
            google_future = executor.submit(fetch_google_links, search_query, search_terms)
            
            # 결과 기다리기
            naver_link_list = naver_future.result()
            google_link_list = google_future.result()

        # 결과를 템플릿으로 전달
        return render(request, 'crawler.html', {
            'page_title': '통합 검색 결과',
            'naver_link_list': naver_link_list,
            'google_link_list': google_link_list,
            'search_query': search_query,
        })

    # GET 요청일 경우 기본 페이지 렌더링
    return render(request, 'crawler.html')
