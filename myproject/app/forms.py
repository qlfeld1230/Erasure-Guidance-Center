from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

''' drf 의 serializer 같은 것
- 장고는 DRF와는 달라서 templates의 html 들을 수정하기 위해서 form 을 수정해야 함
'''
class CustomUserEnrollForm(UserCreationForm):
    
    phone_number = forms.CharField(max_length=15, required=False)
    terms = forms.BooleanField(label="약관에 동의합니다.")
    
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'phone_number','birthday', 'organization' 
        ]
        
    #이메일 유효성 검사
    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError("이미 존재하는 이메일입니다.")
        return email
    
    #약관 동의 확인
    def clean_terms(self):
        terms = self.cleaned_data.get('terms')
        if not terms:
            raise forms.ValidationError("약관에 동의하셔야 합니다.")
        return terms