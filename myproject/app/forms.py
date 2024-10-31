from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser

''' drf 의 serializer 같은 것
- 장고는 DRF와는 달라서 templates의 html 들을 수정하기 위해서 form 을 수정해야 함
'''
class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = [
            'username', 'email', 'password1', 'password2',
            'first_name', 'last_name', 'age', 'address', 'school', 'resident_number'
        ]
