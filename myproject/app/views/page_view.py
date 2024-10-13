from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib import messages
from django.views import View

class MainView(View):
    def get(self, request):
        return render(request, 'main.html')
    
class EnrollView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'enroll.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, '회원가입이 완료되었습니다.')
            return redirect('login')
        else:
            messages.error(request, '회원가입 중 오류가 발생했습니다. 다시 시도해주세요.')
            return render(request, 'enroll.html', {'form': form})
