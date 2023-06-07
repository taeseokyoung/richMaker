from django.db import models
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
from articles.models import Challenge, Comment
import urllib.request
from django.core.files import File
from io import BytesIO
from PIL import Image



class UserManager(BaseUserManager):
    def create_user(self, email, username, password=None):
        if not password:
            raise ValueError('사용자의 비밀번호는 필수 입력 사항 입니다.')
        elif not username:
            raise ValueError('사용자 별명은 필수 입력 사항 입니다.')
        elif not email:
            raise ValueError('사용자 이메일은 필수 입력 사항 입니다.')

        user = self.model(
            email=self.normalize_email(email),
            username=username,
        )
        user.set_password(password)
        user.save(using=self._db)
        return user

    # python manage.py createsuperuser 사용 시 해당 함수가 사용됨
    def create_superuser(self, email, username, password=None):
        user = self.create_user(
            email,
            password=password,
            username=username,
        )
        # 관리자 계정을 생성시 is_admin과 active는 True로 설정
        user.is_admin = True
        user.is_active = True
        user.save(using=self._db)
        return user

class User(AbstractBaseUser):
    email = models.EmailField("이메일 주소", max_length=100, unique=True)
    username = models.CharField("사용자이름", max_length=20)
    password = models.CharField("비밀번호", max_length=128)
    bio = models.TextField(default="아직 소개글이 없습니다.",max_length=200)
    profile_image = models.ImageField(upload_to="%Y/%m", blank=True) # 디렉토리 관리를 년/월기준으로 나눈다.
    auth_code = models.CharField(max_length=20, blank=True)
    created_at = models.DateTimeField("가입일", auto_now_add=True)
    updated_at = models.DateTimeField("수정일", auto_now=True)
    money = models.PositiveIntegerField(default=0)
    is_admin = models.BooleanField(default=False) # 관리자 권한
    is_active = models.BooleanField(default=True) # 계정 활성화
    LOGIN_TYPES = [
        ("normal", "일반"),
        ("kakao", "카카오"),
        ("google", "구글"),
    ]
    login_type = models.CharField(
        "로그인유형", max_length=10, choices=LOGIN_TYPES, default="normal"
    )
    # 챌린지 북마크(첼린지 맴버)
    bookmark = models.ManyToManyField(Challenge, symmetrical=False, related_name='bookmarking_people', blank=True)
    # 첼린지 좋아요(첼린지 관심 등록)
    challenge_like = models.ManyToManyField(Challenge, symmetrical=False,related_name='liking_people', blank=True)

    # 로그인에 필요한 필드 지정
    USERNAME_FIELD = 'email'

    # object를 생성할 때 필수 입력받을 필드 지정
    REQUIRED_FIELDS = ['username','password']
    objects = UserManager()

    def __str__(self):
        return self.username


    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.is_admin


