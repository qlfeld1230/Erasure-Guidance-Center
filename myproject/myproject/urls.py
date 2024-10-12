from django.contrib import admin
from django.urls import path
from app import views

urlpatterns = [
    path('main/', views.main),
    path('login/', views.login),
    path('enroll/', views.enroll),
]
