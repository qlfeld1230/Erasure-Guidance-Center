from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View
from django.urls import reverse_lazy
from ..forms import CustomUserEnrollForm
from ..models import CustomUser

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
    
    def get(self, request):
        # GET 요청 시 폼을 빈 상태로 전달
        form = CustomUserEnrollForm()
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        # POST 요청 시 폼에 사용자 입력을 처리
        form = CustomUserEnrollForm(request.POST)
        if form.is_valid():
            user = form.save()  # 유효하면 데이터베이스에 저장
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect(self.success_url)  # 성공 시 로그인 페이지로 리디렉션
        else:
            # 폼에 오류가 있으면 다시 폼을 렌더링하면서 오류 메시지를 표시
            messages.error(request, '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            return render(request, self.template_name, {'form': form})