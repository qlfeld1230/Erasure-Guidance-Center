from django.shortcuts import render
import requests

def fetch_daum_blog(request):
    query = request.GET.get('query', '')
    posts = []
    error = None

    if query:
        api_key = "98ccdf859ffce97ddad0cc3cb8717e6c"
        headers = {"Authorization": f"KakaoAK {api_key}"}
        url = "https://dapi.kakao.com/v2/search/blog"
        params = {"query": query, "sort": "recency", "page": 1, "size": 10}

        response = requests.get(url, headers=headers, params=params)

        if response.status_code == 200:
            data = response.json()
            posts = data.get("documents", [])
        else:
            error = "API 요청 실패. 다시 시도해주세요."

    return render(request, 'daum_api.html', {"posts": posts, "error": error})