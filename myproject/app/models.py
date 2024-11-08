from django.db import models
from django.contrib.auth.models import AbstractUser

''' 개요
- 커스텀 유저 테이블
'''

''' 커스텀 회원 가입
- 장고는 기본으로 DB에 대한 model을 제공을 해줍니다.
- 먼저 알아보시기 편하게 명시적으로 id ~ last_login 까지 적어뒀습니다. 이건 장고에서 base로 제공해주는 것입니다.
- 그 다음 밑에 있는 것들을 추가해 나가면서 migrations, migrate 하시면 SQL에 반영이 됩니다.
'''
class CustomUser(AbstractUser):
    # 기본 필드 명시
    id = models.AutoField(primary_key=True)                     # 유저의 id 입니다. 번호입니다. primary_key 1부터 시작해요
    username = models.CharField(max_length=150, unique=True)    # 이게 실질적인 id 입니다. 
    password = models.CharField(max_length=128)                 # 비밀번호
    first_name = models.CharField(max_length=150, blank=True)   # 이름
    last_name = models.CharField(max_length=150, blank=True)    # 성
    email = models.EmailField(blank=True)                       # 이메일
    is_staff = models.BooleanField(default=False)               # 서비스의 운영자인지, 소비자인지
    is_active = models.BooleanField(default=True)               # 지금 로그인해있는지, 로그아웃인지
    date_joined = models.DateTimeField(auto_now_add=True)       # 가입 날짜
    last_login = models.DateTimeField(null=True, blank=True)    # 최근 로그인 날짜

    # 커스텀 필드
    age = models.PositiveIntegerField(null=True, blank=True)      # 나이
    address = models.CharField(max_length=255, blank=True)        # 주소 필드
    school = models.CharField(max_length=100, blank=True)         # 학교 필드
    resident_number = models.CharField(max_length=15, blank=True) # 주민번호
    


