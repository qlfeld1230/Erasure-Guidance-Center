from django.contrib import admin
from django.urls import path
from app.views.homepage_view import MainView, EnrollView
from django.contrib.auth.views import LogoutView, LoginView

from app.views.youtube_view import *
from app.views.meta_view import *
from app.views.naver_view import *
from app.views.kakao_view import *

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
    path('', MainView.as_view()),

    # 회원 가입 및 로그인 관련 및 홈 크롤러
    path('homepage/login/', LoginView.as_view(template_name='homepage_login.html', success_url='/'), name='homepage_login'), 
    path('homepage/logout/', LogoutView.as_view(next_page='homepage_login/')), 
    path('homepage/enroll/', EnrollView.as_view()), 
    
    # 페이스북 관련 API 및 콜백
    path('facebook/login/', Facebook.login, name='facebook_login'),
    path('facebook/callback/', Facebook.callback, name='facebook_callback'),
    path('facebook/posts/', Facebook.posts, name='facebook_posts'),

    # 인스타그램 관련 API 및 콜백
    path('instagram/login/', Instagram.login, name='instagram_login'),
    path('instagram/callback/', Instagram.callback, name='instagram_callback'),
    path('instagram/posts/', Instagram.posts, name='instagram_posts'),

    # 네이버
    path('naver/', Naver.web_search, name='naver_search'),
    path('naver_rss/', Naver_rss.rss),
    path('cafe_search/', Naver.cafe_search, name='cafe_search'),

    # 다음
    path('daum/', daum.daum_search, name='daum_search'),
    
    # 트위터
    # 인스타그램
    
    # 유튜브 댓글
    path('youtube/', redirect_to_google_activity, name='redirect_to_google_activity'),
    
    
]
