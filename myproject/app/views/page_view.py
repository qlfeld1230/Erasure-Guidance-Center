from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import View

from app.forms import CustomUserEnrollForm


class IndexView(View):
    def get(self, request):
        return render(request, 'index.html')


class MainView(View):
    def get(self, request):
        return render(request, 'main.html')

    def post(self, request):
        return render(request, 'main.html')


class EnrollView(View):
    template_name = 'enroll.html'
    form_class = CustomUserEnrollForm
    success_url = reverse_lazy('homepage_login')

    def get(self, request):
        form = self.form_class()  # CustomUserEnrollForm을 사용
        return render(request, self.template_name, {'form': form})

    def post(self, request):
        form = self.form_class(request.POST)  # CustomUserEnrollForm을 사용
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect(self.success_url)
        else:
            messages.error(request, '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            return render(request, self.template_name, {'form': form})
