from django.shortcuts import render, redirect
from django.conf import settings
import requests


class Instagram:
    
    ''' 인스타 로그인
    '''
    @staticmethod
    def login(request):
        client_id = settings.INSTAGRAM_APP_ID
        redirect_uri = settings.INSTAGRAM_REDIRECT_URI
        scope = "user_profile,user_media"
        return redirect(f"https://api.instagram.com/oauth/authorize?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}&response_type=code")
    
    ''' 인스타 콜백 함수
    '''
    @staticmethod
    def callback(request):
        code = request.GET.get("code")
        client_id = settings.INSTAGRAM_APP_ID
        client_secret = settings.INSTAGRAM_APP_SECRET
        redirect_uri = settings.INSTAGRAM_REDIRECT_URI

        token_url = "https://api.instagram.com/oauth/access_token"
        data = {
            "client_id": client_id,
            "client_secret": client_secret,
            "grant_type": "authorization_code",
            "redirect_uri": redirect_uri,
            "code": code,
        }
        
        response = requests.post(token_url, data=data)
        access_token = response.json().get("access_token")
        
        request.session['instagram_access_token'] = access_token
        return redirect("instagram_posts")
    
    ''' 인스타 포스트
    '''
    @staticmethod
    def posts(request):
        access_token = request.session.get('instagram_access_token')
        
        if not access_token:
            return redirect("instagram_login")

        url = "https://graph.instagram.com/me/media"
        params = {
            "access_token": access_token,
            "fields": "caption,media_url,timestamp"
        }

        response = requests.get(url, params=params)
        posts = []

        if response.status_code == 200:
            data = response.json().get("data", [])
            for item in data:
                post = {
                    "caption": item.get("caption", ""),
                    "media_url": item.get("media_url", ""),
                    "timestamp": item.get("timestamp", ""),
                    "id": item.get("id")
                }
                posts.append(post)

        return render(request, "instagram_api.html", {"posts": posts})
    
    
class Facebook:
    
    ''' 페이스북 로그인
    - 페이스북 로그인을 시작하는 함수입니다. Facebook OAuth 대화 상자로 리디렉션하여 사용자가 권한을 승인하도록 유도
    '''
    @staticmethod
    def login(request):
        client_id = settings.FACEBOOK_APP_ID
        redirect_uri = settings.FACEBOOK_REDIRECT_URI
        scope = "user_posts"
        return redirect(f"https://www.facebook.com/v21.0/dialog/oauth?client_id={client_id}&redirect_uri={redirect_uri}&scope={scope}")
    
    ''' 페이스북 콜백 함수
    - 사용자가 로그인 인증 후 리디렉션되는 콜백 함수입니다. code를 받아 액세스 토큰을 요청하고 세션에 저장한 뒤 facebook_posts로 리디렉션합니다.
    '''
    @staticmethod
    def callback(request):
        code = request.GET.get("code")
        client_id = settings.FACEBOOK_APP_ID
        client_secret = settings.FACEBOOK_APP_SECRET
        redirect_uri = settings.FACEBOOK_REDIRECT_URI

        token_url = f"https://graph.facebook.com/v21.0/oauth/access_token?client_id={client_id}&redirect_uri={redirect_uri}&client_secret={client_secret}&code={code}"
        token_response = requests.get(token_url)
        access_token = token_response.json().get("access_token")
        request.session['facebook_access_token'] = access_token

        return redirect("facebook_posts")
    
    ''' 페이스북 포스트
    - 페이스북에서 사용자의 게시글을 가져오는 함수입니다. facebook_callback에서 저장된 액세스 토큰을 세션에서 가져와 Graph API를 통해 게시글을 요청합니다.
    '''
    @staticmethod
    def posts(request):
        access_token = request.session.get('facebook_access_token')

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

        if response.status_code == 200:
            data = response.json().get("data", [])
            for item in data:
                post = {
                    "message": item.get("message", ""),
                    "created_time": item.get("created_time", ""),
                    "id": item.get("id")
                }
                posts.append(post)

        return render(request, "facebook_api.html", {"posts": posts})

