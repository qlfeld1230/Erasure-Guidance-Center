from django.shortcuts import render
from django.conf import settings
import requests


class daum:
    ''' 다음 API 통합 검색 '''
    
    @staticmethod
    def daum_search(request):
        query = request.GET.get('query', '')
        web_posts, blog_posts, cafe_posts = [], [], []
        error = None

        if query:
            rest_api_key = settings.KAKAO_REST_API_KEY
            headers = {"Authorization": f"KakaoAK {rest_api_key}"}
            base_url = "https://dapi.kakao.com/v2/search/"
            params = {"query": query, "sort": "recency", "page": 1, "size": 10}
            
            try:
                # 웹 검색 요청
                web_response = requests.get(f"{base_url}web", headers=headers, params=params)
                if web_response.status_code == 200:
                    web_data = web_response.json()
                    web_posts = web_data.get("documents", [])
                else:
                    error = "웹 검색 API 요청 실패."

                # 블로그 검색 요청
                blog_response = requests.get(f"{base_url}blog", headers=headers, params=params)
                if blog_response.status_code == 200:
                    blog_data = blog_response.json()
                    blog_posts = blog_data.get("documents", [])
                else:
                    error = "블로그 검색 API 요청 실패."

                # 카페 검색 요청
                cafe_response = requests.get(f"{base_url}cafe", headers=headers, params=params)
                if cafe_response.status_code == 200:
                    cafe_data = cafe_response.json()
                    cafe_posts = cafe_data.get("documents", [])
                else:
                    error = "카페 검색 API 요청 실패."
            
            except requests.RequestException as e:
                error = f"API 요청 오류: {e}"

        context = {
            "web_posts": web_posts,
            "blog_posts": blog_posts,
            "cafe_posts": cafe_posts,
            "error": error
        }
        return render(request, 'daum_api.html', context)

    
class Kakao:
    
    def temp():
        return