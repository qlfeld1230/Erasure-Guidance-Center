from django.contrib import admin
from django.urls import path
from app.views.homepage_view import MainView, EnrollView
from app.views.crawler_view import *
from django.contrib.auth.views import LogoutView, LoginView
from django.contrib.auth.views import LoginView
from django.shortcuts import render
from app.forms import CustomUserEnrollForm
from app.models import CustomUser
from django.urls import reverse_lazy
from app.views.homepage_view import CustomLogoutView
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
    
     # Django Admin 페이지 URL
    path('admin/', admin.site.urls),
    
    # 회원 가입 및 로그인 관련 및 홈 크롤러
    path('homepage/login/', LoginView.as_view(template_name='homepage_login.html'), name='homepage_login'), 
    path('homepage/logout/', CustomLogoutView.as_view(), name = 'homepage_logout'), 
    path('homepage/enroll/', EnrollView.as_view(), name = 'homepage_enroll'), 
    path('homepage/crawler/', integrated_crawler_view),

]