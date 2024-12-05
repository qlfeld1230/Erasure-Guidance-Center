from django.shortcuts import render
from django.contrib.auth import logout
from django.shortcuts import redirect

def main(request):
    return render(request, 'main.html')

def login(request):
    return render(request, 'login.html')

def enroll(request):
    return render(request, 'enroll.html')
