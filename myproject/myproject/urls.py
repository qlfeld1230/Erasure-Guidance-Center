from django.contrib import admin
from django.urls import path
from app.views.page_view import MainView, EnrollView, IndexView
from app.views.crawler_view import *

from django.contrib.auth.views import LogoutView, LoginView

urlpatterns = [
    path('', IndexView.as_view(), name='index'),
    path('main/', MainView.as_view(), name='main'),
    path('admin/', admin.site.urls),
    path('login/', LoginView.as_view(template_name='login.html', success_url='/')),
    path('logout/', LogoutView.as_view(next_page='/login/')),
    path('enroll/', EnrollView.as_view()),
    path('crawler/', integrated_crawler_view),
]
