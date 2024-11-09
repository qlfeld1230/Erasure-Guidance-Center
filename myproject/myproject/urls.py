from django.contrib import admin
from django.urls import path
from app.views.homepage_view import MainView, EnrollView
from app.views.homepage_crawler_view import *
from app.views.facebook_api_view import *
from app.views.naver_rss_view import *
from django.contrib.auth.views import LogoutView, LoginView
from app.views.daum_api_view import fetch_daum_blog
from django.shortcuts import render
from app.forms import CustomUserEnrollForm
from app.models import CustomUser

''' 개요
- 홈
- 페이스북
- 네이버
- 다음
'''

urlpatterns = [
    # Admin 페이지
    # path('admin/', admin.site.urls), 

    # 메인 페이지 (앱 진입점)
    path('', MainView.as_view(), name = 'main'),

    # 회원 가입 및 로그인 관련 및 홈 크롤러
    path('homepage/login/', LoginView.as_view(template_name='homepage_login.html'), name='homepage_login'), 
    path('homepage/logout/', LogoutView.as_view(next_page='homepage_/login/')), 
    path('homepage/enroll/', EnrollView.as_view(), name = 'homepage_enroll'), 
    path('homepage/crawler/', integrated_crawler_view),
    
    # 페이스북 관련 API 및 콜백
    path('facebook/login/', facebook_login, name='facebook_login'),
    path('facebook/callback/', facebook_callback, name='facebook_callback'), 
    path('facebook/posts/', facebook_posts, name='facebook_posts'), 
    
    # 네이버 rss 
    path('naver/', fetch_naver_rss, name='fetch_naver_rss'),
    path('nvaer/rss/', lambda request: render(request, 'naver_rss.html'), name='fetch_naver_rss_request'),
    
    # 다음
    path('daum/', fetch_daum_blog, name='fetch_daum_blog'),
    # 카카오 스토리 크롤링
    # 브런치 스토리 크롤링
    
    
    # 트위터
    # 인스타그램
    


]