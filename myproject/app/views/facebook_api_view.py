from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.decorators import login_required
import requests

''' 개요
facebook_login     로그인 시작.
facebook_callback  콜백 처리 및 액세스 토큰 저장.
facebook_posts     토큰을 사용하여 페이스북 게시글을 요청.
'''


''' 페이스북 로그인
- 페이스북 로그인을 시작하는 함수입니다. Facebook OAuth 대화 상자로 리디렉션하여 사용자가 권한을 승인하도록 유도
'''
def facebook_login(request):
    client_id = settings.FACEBOOK_APP_ID
    redirect_uri = settings.FACEBOOK_REDIRECT_URI
    scope = "user_posts"
    return redirect(f"https://www.facebook.com/v21.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}")

''' 페이스북 콜백 함수
- 사용자가 로그인 인증 후 리디렉션되는 콜백 함수입니다. code를 받아 액세스 토큰을 요청하고 세션에 저장한 뒤 facebook_posts로 리디렉션합니다.
'''
def facebook_callback(request):
    code = request.GET.get("code")
    client_id = settings.FACEBOOK_APP_ID
    client_secret = settings.FACEBOOK_APP_SECRET
    redirect_uri = settings.FACEBOOK_REDIRECT_URI

    # Access Token 요청
    token_url = f"https://graph.facebook.com/v21.0/oauth/access_token?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
    token_response = requests.get(token_url)
    access_token = token_response.json().get("access_token")

    # Access Token을 세션에 저장
    request.session['facebook_access_token'] = access_token

    return redirect("facebook_posts")

''' 페이스북 포스트
- 페이스북에서 사용자의 게시글을 가져오는 함수입니다. facebook_callback에서 저장된 액세스 토큰을 세션에서 가져와 Graph API를 통해 게시글을 요청합니다.
'''
def facebook_posts(request):
    access_token = request.session.get('facebook_access_token')

    # Access Token이 없는 경우 로그인 리디렉션
    if not access_token:
        return redirect("facebook_login")

    url = "https://graph.facebook.com/v21.0/me/posts"
    params = {
        "access_token": access_token,
        "fields": "message,created_time"
    }

    # Graph API 요청
    response = requests.get(url, params=params)
    posts = []

    # 응답이 성공적이면 데이터를 파싱
    if response.status_code == 200:
        data = response.json().get("data", [])
        for item in data:
            post = {
                "message": item.get("message", ""),
                "created_time": item.get("created_time", ""),
                "id": item.get("id")
            }
            posts.append(post)

    # 템플릿에 데이터를 전달
    return render(request, "facebook_api.html", {"posts": posts})
