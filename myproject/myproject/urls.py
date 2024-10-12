from django.contrib import admin
from django.urls import path
from app.views.page_view import *
from app.views.crawler_view import *

urlpatterns = [
    path('main/', main),
    path('login/', login),
    path('enroll/', enroll),
    
    path('crawler/', crawler_view),

]
