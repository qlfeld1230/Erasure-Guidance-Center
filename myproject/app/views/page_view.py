from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from ..forms import CustomUserCreationForm

''' 페이지 뷰 개요
- EnrollView 는 회원 가입에 사용하는 컨트롤러(뷰) 입니다.
- MainView 는 메인 페이지에 관련된 뷰를 만들겁니다.
- 
'''

''' 메인 뷰
- main.html 랜더링 해줌 / 특별한 기능은 없음 현재
'''
class MainView(View):
    def get(self, request):
        return render(request, 'main.html')

''' 회원 가입
- get 및 form 으로 페이지 가져오고
- post 로 회원 가입 로직
- post 성공시 login.html 로 리다이렉트
'''
class EnrollView(View):
    def get(self, request):
        form = CustomUserCreationForm()
        return render(request, 'enroll.html', {'form': form})

    def post(self, request):
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')
        else:
            messages.error(request, '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            return render(request, 'enroll.html', {'form': form})