from django.contrib import admin
from django.urls import path
from app.views.homepage_view import MainView, EnrollView
from app.views.crawler_view import integrated_crawler_view
from django.contrib.auth.views import LogoutView, LoginView

from app.views.youtube_view import *
from app.views.meta_view import *
from app.views.naver_view import *
from app.views.kakao_view import *
from app.views.homepage_view import *
from app.views.page_view import *
from app.views.X_view import *

''' 개요
- 홈
- 페이스북
- 네이버
- 다음
'''

urlpatterns = [
    # 메인 페이지 (앱 진입점)
    path('', IndexView.as_view(), name='index'),
    path('main/', MainView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html',
         success_url='/'), name='login'),
    path('logout/', LogoutView.as_view(next_page='/'), name='logout'),
    path('crawler/', integrated_crawler_view),
    path('consent/', ConsentView.as_view(),
         name='consent'),  # 개인정보 수집 및 이용 동의 페이지 URL
    path('introduce/', IntroduceView.as_view(),
         name='introduce'),
    path('privacy-policy/', Privacy_policyView.as_view(),
         name='privacy-policy'),

    path('consent/enroll/', EnrollView.as_view(), name='enroll'),


    # path('', MainView.as_view(), name = 'main'),

    # Django Admin 페이지 URL
    path('admin/', admin.site.urls),

    # 회원 가입 및 로그인 관련 및 홈 크롤러
#     path('homepage/login/', LoginView.as_view(template_name='homepage_login.html'),
#          name='homepage_login'),
#     path('homepage/logout/', CustomLogoutView.as_view(), name='homepage_logout'),
#     path('homepage/enroll/', EnrollView.as_view(), name='homepage_enroll'),
#     path('homepage/crawler/', integrated_crawler_view),

    # # 회원 가입 및 로그인 관련 및 홈 크롤러
    # path('homepage/login/', LoginView.as_view(template_name='homepage_login.html', success_url='/'), name='homepage_login'),
    # path('homepage/logout/', LogoutView.as_view(next_page='homepage_login/')),
    # path('homepage/enroll/', EnrollView.as_view()),

    # 페이스북 관련 API 및 콜백
    path('main/facebook/login/', Facebook.login, name='facebook_login'),
    path('main/facebook/callback/', Facebook.callback, name='facebook_callback'),
    path('main/facebook/posts/', Facebook.posts, name='facebook_posts'),

    # 인스타그램 관련 API 및 콜백
    path('main/instagram/login/', Instagram.login, name='instagram_login'),
    path('main/instagram/callback/', Instagram.callback, name='instagram_callback'),
    path('main/instagram/posts/', Instagram.posts, name='instagram_posts'),

    # 네이버
    # path('naver/', Naver.web_search, name='naver_search'),
    path('main/naver_rss/', Naver_rss.rss, name='naver_rss'),

    # 유튜브 댓글
    path('youtube/', redirect_to_google_activity,
         name='redirect_to_google_activity'),

    # 트위터
    path('twitter/', redirect_to_twitter_home, name='redirect_to_twitter_home'),

]
