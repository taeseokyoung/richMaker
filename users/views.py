from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import ComtomTokenObtainPairSerializer

# Create your views here.
class UserView(APIView):
    # 회원 정보 수정
    def put(self,request):
        pass
    # 휴면 계정으로 전환
    def delete(self,request):
        pass

class ProfileView(APIView):
    # 프로필 정보 읽기
    def get(self,request):
        pass
    # 프로필 정보 수정
    def put(self,request):
        pass
    # 수입,지출 관리
    def fetch(self,request):
        pass

class UserAPIView(APIView):
    # 회원 가입
    def post(self,request):
        pass

class UserLikes(APIView):
    # like 등록
    def post(self, request):
        pass
    # like 수정
    def put(self,request):
        pass

class UserBookMark(APIView):
    # bookMark 등록
    def post(self, request):
        pass
    # bookMark 수정
    def put(self,request):
        pass

class UserWish(APIView):
    # 찜목록 등록
    def post(self, request):
        pass



class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComtomTokenObtainPairSerializer