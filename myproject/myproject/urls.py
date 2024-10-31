from django.contrib import admin
from django.urls import path
from app.views.page_view import MainView, EnrollView
from app.views.crawler_view import *
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    # 메인 페이지
    path('', MainView.as_view()),
    
    # 회원 가입 및 로그인 관련 -> logout 은 url 처리하면 안 됨, 나중에 수정할 것
    path('admin/', admin.site.urls), 
    path('login/', LoginView.as_view(template_name='login.html', success_url='/'), name='login'),  # name 추가
    path('logout/', LogoutView.as_view(next_page='/login/')), 
    path('enroll/', EnrollView.as_view()),
    
    # 크롤러 페이지
    path('crawler/', integrated_crawler_view),
]