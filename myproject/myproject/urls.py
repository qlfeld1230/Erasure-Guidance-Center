from django.contrib import admin
from django.urls import path
from app.views.page_view import MainView, EnrollView
# 수정됨
from app.views.crawler_view_sunho import *
from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', MainView.as_view()),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html', success_url='/')),
    path('logout/', LogoutView.as_view(next_page='/login/')),
    path('enroll/', EnrollView.as_view()),
    path('crawler/', integrated_crawler_view),
]
