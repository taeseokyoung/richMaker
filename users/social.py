from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
import os
from rest_framework_simplejwt.tokens import RefreshToken
from .models import User
from .serializer import CustomTokenObtainPairSerializer
from django.core.files.base import ContentFile
import requests
import urllib.request


REDIRECT_URI = 'http://127.0.0.1:5501/test.html'
KAKAO_API = os.environ.get('KAKAO_API')
KAKAO_CLIENT = os.environ.get('KAKAO_CLIENT')



class KakaoLogin(APIView):
    """카카오 소셜 로그인"""
    def get(self, request):
        """ USER가 요청한 API키 발급 """
        return Response(KAKAO_API, status=status.HTTP_200_OK)

    def post(self, request):
        """ Resource Server가 발급해준 Code 확인 """
        auth_code = request.data.get("code")
        kakao_token_api = "https://kauth.kakao.com/oauth/token"
        data = {
            "grant_type": "authorization_code",
            "client_id": KAKAO_API,
            "redirect_uri": REDIRECT_URI,
            "code": auth_code,
        }
        kakao_token = requests.post(
            kakao_token_api,
            headers={"Content-Type": "application/x-www-form-urlencoded"},
            data=data,

        )
        access_token = kakao_token.json().get("access_token")
        user_data = requests.get(
            "https://kapi.kakao.com/v2/user/me",
            headers={
                "Authorization": f"Bearer {access_token}",
                "Content-type": "application/x-www-form-urlencoded;charset=utf-8",
            },
        )
        user_data = user_data.json()
        print(user_data.get("properties").get("profile_image"))
        try:
            data = {
                "profile_image": user_data.get("properties").get("profile_image"),
                "username": user_data.get("properties").get("nickname"),
                "email": user_data.get("kakao_account").get("email"),
                "login_type": "kakao",
            }
        except AttributeError:
            return Response({"message": "유효하지 않은 토큰입니다."}, status=status.HTTP_401_UNAUTHORIZED)

        return SocialLogin(**data)

def SocialLogin(**kwargs):
    """소셜 로그인, 회원가입"""
    # 각각 소셜 로그인에서 email, nickname, login_type등을 받아옴!!
    data = {k: v for k, v in kwargs.items() if v is not None}
    print(f'이미지 출력 테스트 : {data.get("profile_image")}')
    email = data.get("email")
    login_type = data.get("login_type")
    if not email:
        return Response({"error": "해당 계정에 email정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
    try:
        user = User.objects.get(email=email)
        # 로그인 타입까지 같으면, 토큰 발행해서 프론트로 보내주기
        if login_type == user.login_type:
            refresh = RefreshToken.for_user(user)
            access_token = CustomTokenObtainPairSerializer.get_token(user)
            return Response({"refresh": str(refresh), "access": str(access_token.access_token)},status=status.HTTP_200_OK)
        else:
            # 유저의 다른 소셜계정으로 로그인한 유저라면, 해당 로그인 타입을 보내줌.
            return Response({"error": f"{user.login_type}으로 이미 가입된 계정이 있습니다!"},status=status.HTTP_400_BAD_REQUEST,)

    # 유저가 존재하지 않는다면 회원가입시키기
    except User.DoesNotExist:
        new_user = User.objects.create(**data)
        



        # pw는 사용불가로 지정
        new_user.set_unusable_password()
        # new_user.save()

        # 이후 토큰 발급해서 프론트로
        refresh = RefreshToken.for_user(new_user)
        access_token = CustomTokenObtainPairSerializer.get_token(new_user)
        return Response({"refresh": str(refresh), "access": str(access_token.access_token)},status=status.HTTP_200_OK,)