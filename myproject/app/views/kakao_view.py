from django.shortcuts import render
from django.conf import settings
import requests


class daum:
    
    ''' 다음 API 검색
    '''
    def web_search(request):
        query = request.GET.get('query', '')
        posts = []
        error = None

        if query:
            rest_api_key = settings.KAKAO_REST_API_KEY
            headers = {"Authorization": f"KakaoAK {rest_api_key}"}
            url = "https://dapi.kakao.com/v2/search/web"
            params = {"query": query, "sort": "recency", "page": 1, "size": 10}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                posts = data.get("documents", [])
            else:
                error = "API 요청 실패. 다시 시도해주세요."

        return render(request, 'daum_api.html', {"posts": posts, "error": error})
    
    ''' 다음 API 블로그 검색
    '''
    def blog_search(request):
        query = request.GET.get('query', '')
        posts = []
        error = None

        if query:
            rest_api_key = settings.KAKAO_REST_API_KEY
            headers = {"Authorization": f"KakaoAK {rest_api_key}"}
            url = "https://dapi.kakao.com/v2/search/blog"
            params = {"query": query, "sort": "recency", "page": 1, "size": 10}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                posts = data.get("documents", [])
            else:
                error = "API 요청 실패. 다시 시도해주세요."

        return render(request, 'daum_api.html', {"posts": posts, "error": error})
    
    ''' 다음 API 카페 검색
    '''
    def cafe_search(request):
        query = request.GET.get('query', '')
        posts = []
        error = None

        if query:
            rest_api_key = settings.KAKAO_REST_API_KEY
            headers = {"Authorization": f"KakaoAK {rest_api_key}"}
            url = "https://dapi.kakao.com/v2/search/cafe"
            params = {"query": query, "sort": "recency", "page": 1, "size": 10}

            response = requests.get(url, headers=headers, params=params)

            if response.status_code == 200:
                data = response.json()
                posts = data.get("documents", [])
            else:
                error = "API 요청 실패. 다시 시도해주세요."

        return render(request, 'daum_api.html', {"posts": posts, "error": error})
    
    
class Kakao:
    
    def empty():
        return