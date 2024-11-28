from django.shortcuts import render, redirect
from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.views import View
from django.urls import reverse_lazy
from ..forms import CustomUserEnrollForm
from ..models import CustomUser
from django.contrib.auth.views import LogoutView
from django.contrib.auth import logout
import os
import django
import sys

sys.path.append("C:/Users/sej68/Documents/GitHub/Erasure-Guidance-Center/myproject")
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "myproject.settings")
django.setup()

''' 개요
- EnrollView 는 회원 가입에 사용하는 컨트롤러(뷰) 입니다.
- MainView 는 메인 페이지에 관련된 뷰를 만들겁니다.
'''

''' 메인 뷰
- main.html 랜더링 해줌 / 특별한 기능은 없음 현재
'''
class MainView(View):
    def get(self, request):
        return render(request, 'homepage_main.html')

''' 회원 가입
- get 및 form 으로 페이지 가져오고
- post 로 회원 가입 로직
- post 성공시 login.html 로 리다이렉트
'''
class EnrollView(View):
    model = CustomUser
    template_name = 'homepage_enroll.html'
    success_url = reverse_lazy('homepage_login') # 성공 시 login 페이지로 리다이렉션
   
    def dispatch(self, request, *args, **kwargs):
        if request.method == "POST":
            return self.post(request)
        return self.get(request)

    def get(self, request):
        form = CustomUserEnrollForm()
        return render(request, self.template_name, {'form': form})
        
    def post(self, request):
        form = CustomUserEnrollForm(request.POST)
        if form.is_valid():
            # 회원가입 저장
            user = form.save()
            username = form.cleaned_data.get('username')
            raw_password = form.cleaned_data.get('password1')

            # 사용자 인증 후 로그인
            user = authenticate(username=username, password1=raw_password)
            if user is not None:
                login(request, user)
                messages.success(request, "회원가입과 로그인 성공!")
                print('로그인 성공')
                return redirect('main')  # 메인 페이지로 리다이렉트
            else:
                messages.error(request, "사용자 인증에 실패했습니다.")
                return redirect(self.success_url)
        else:
            # 폼 오류 출력
            print('로그인 실패')
            print(form.errors)  # 오류 메시지 출력
            messages.error(request, "회원가입 중 오류가 발생했습니다.")
            return render(request, self.template_name, {'form': form, 'errors': form.errors})

class CustomLogoutView(LogoutView):
    def post(self, request, *args, **kwargs):
        logout(request)  # 로그아웃 처리
        return redirect('main')  # 로그아웃 후 로그인 페이지로 리다이렉트
     
    # GET 요청은 처리하지 않도록 명시적으로 설정
    def get(self, request, *args, **kwargs):
        return redirect('main')  # GET 요청이 오면 로그인 페이지로 리다이렉트