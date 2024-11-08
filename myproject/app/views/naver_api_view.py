from django.shortcuts import render, redirect
from django.conf import settings
import requests

''' 개요
naver_cafe_login     네이버 카페 로그인 시작.
naver_callback       콜백 처리 및 액세스 토큰 저장.
naver_cafe_posts     네이버 카페에서 게시글 목록 요청.
'''

def naver_cafe_login(request):
    client_id = settings.NAVER_CLIENT_ID
    redirect_uri = settings.NAVER_REDIRECT_URI
    state = "random_state_string"  # 보안을 위한 state 값 설정
    return redirect(f"https://nid.naver.com/oauth2.0/authorize?response_type=code&client_id={client_id}&redirect_uri={redirect_uri}&state={state}")

def naver_callback(request):
    code = request.GET.get("code")
    state = request.GET.get("state")
    client_id = settings.NAVER_CLIENT_ID
    client_secret = settings.NAVER_CLIENT_SECRET

    # Access Token 요청
    token_url = "https://nid.naver.com/oauth2.0/token"
    params = {
        "grant_type": "authorization_code",
        "client_id": client_id,
        "client_secret": client_secret,
        "code": code,
        "state": state
    }
    token_response = requests.get(token_url, params=params)
    access_token = token_response.json().get("access_token")

    # Access Token을 세션에 저장
    request.session['naver_access_token'] = access_token

    return redirect("naver_cafe_posts")

def naver_cafe_posts(request):
    access_token = request.session.get('naver_access_token')

    # Access Token이 없는 경우 로그인 리디렉션
    if not access_token:
        return redirect("naver_cafe_login")

    # 네이버 카페 게시글 API 요청 URL
    cafe_id = "YOUR_CAFE_ID"  # 네이버 카페 ID 입력
    url = f"https://openapi.naver.com/v1/cafe/{cafe_id}/posts"
    headers = {
        "Authorization": f"Bearer {access_token}"
    }
    params = {
        "query": "카페 게시글",  # 검색할 키워드
        "display": 10           # 가져올 게시글 수 (최대 100)
    }

    # 카페 게시글 API 요청
    response = requests.get(url, headers=headers, params=params)
    posts = []

    # 응답이 성공적이면 데이터를 파싱
    if response.status_code == 200:
        data = response.json().get("items", [])
        for item in data:
            post = {
                "title": item.get("title"),
                "link": item.get("link"),
                "description": item.get("description"),
                "postdate": item.get("postdate")
            }
            posts.append(post)

    # 템플릿에 데이터를 전달
    return render(request, "naver_cafe_posts.html", {"posts": posts})
