from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import (CustomTokenObtainPairSerializer, ProfileUserSerializer, UserSerializer,GetBookmarkUserInfo,GetCommentLikeUserInfo,GetLikingChallengeSerializer,GetBookingChallengeSerializer)
from .models import User
from . import validated
from articles.models import Challenge
from django.contrib.auth.hashers import check_password
from rest_framework_simplejwt.tokens import RefreshToken, AccessToken
import requests

import os




class GetLikingChallenge(APIView):
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer =  GetLikingChallengeSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetBookingChallenge(APIView):
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer =  GetBookingChallengeSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)




class UserProfile(APIView):
    def patch(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        if request.user != owner:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if not validated.validated_username(request.data['username']):
            return Response({"message": "닉네임을 올바르게 작성해 주세요."}, status=status.HTTP_400_BAD_REQUEST)

        serializer = ProfileUserSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message": "프로필을 수정 했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserView(APIView):
    # 프로필 정보 읽어오기
    def get(self,request,user_id):
        owner = get_object_or_404(User, id=user_id)
        serializer = ProfileUserSerializer(owner)
        return  Response(serializer.data ,status=status.HTTP_200_OK)
    # 회원 정보 수정
    def put(self, request, user_id):
        owner = get_object_or_404(User, id=user_id)
        # 인증을 위해, 데이터베이스에 저장된 비밀번호와, 사용자가 입력한 비밀번호가 일치하지 않을 경우
        if not check_password(request.data['auth_code'] ,owner.password):
            return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_401_UNAUTHORIZED)
        # 변경하고자 하는 비밀번호가,  기존의 비밀번호와 일치할 경우
        elif check_password(request.data['password'],owner.password):
            return Response({"message": "기존의 비밀번호로 변경할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if True != validated.validated_password(request.data['password']):
            return Response({"message": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 회원 정보 수정에서 유저네임도 변경하는 기능을 추가한다면 사용할 코드
        # elif True != validated.validated_username(request.data['username']):
        #     return Response({"message": "유저네임이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if request.user == owner:
            serializer = UserSerializer(owner,data=request.data,partial=True) # partial=True : 부분 업데이트
            if serializer.is_valid():
                serializer.save()
                owner.is_active = False
                owner.save()
                return Response({"message": "회원 정보를 수정 했습니다."},status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 휴면 계정으로 전환
    def delete(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if not check_password(request.data['password'],owner.password):
            return Response({"message": "비밀번호가 일치하지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        if request.user == owner:
            owner.is_active = False
            owner.save()
            return Response({"message": "휴면 계정으로 전환 되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"로그인 유효시간이 지났거나,권한이 없습니다."},status=status.HTTP_401_UNAUTHORIZED)

    # 프로필 정보 수정
    def patch(self,request,user_id):
        if not validated.validated_username(request.data['username']):
            return Response({"message": "이름이 잘못되었습니다! (1~20자, 공백x)"}, status=status.HTTP_400_BAD_REQUEST)
        # 400,200,404
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            serializer = ProfileUserSerializer(owner,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"회원 정보를 수정 했습니다."},status=status.HTTP_200_OK)
            else:
                return Response({"message": "올바른 입력값이 아닙니다."},status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"message": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

class GetAuthTokenAPIView(APIView):
    # 이메일 발급 요청(비밀번호 찾기에 사용)
    def post(self, request):
        owner = get_object_or_404(User, email=request.data['email'])
        owner.auth_code = validated.send_email(owner.email)
        owner.save()
        return Response({"message": "인증 메일을 발송 했습니다."}, status=status.HTTP_200_OK)

class UserAPIView(APIView):

    # 회원 가입
    def post(self,request):
        validated_result = validated.validated_data(request.data['email'],request.data['password'],request.data['username'])
        if validated_result != True:
            return Response({'message': validated_result}, status=status.HTTP_401_UNAUTHORIZED)
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            email = serializer.validated_data.get("email")
            owner = get_object_or_404(User,email=email)
            owner.auth_code = validated.send_email(email)
            owner.save()

            return Response({'message':'가입 되셨습니다. 이메일 인증을 해주세요.'},status=status.HTTP_200_OK)
        else:
            return Response({'message':serializer.errors},status=status.HTTP_400_BAD_REQUEST)

    # 이메일 인증
    def put(self,request):
        owner = get_object_or_404(User,email = request.data['email'])
        if owner.auth_code == '':
            return Response({"message":"먼저 인증코드를 발급받아주세요."},status=status.HTTP_400_BAD_REQUEST)
        elif not owner.auth_code == request.data['auth_code']:
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_401_UNAUTHORIZED)
        owner.auth_code = ''
        owner.is_active = True
        owner.save()
        # 인증 메일 요청
        return Response({"message":"인증 되었습니다."},status=status.HTTP_200_OK)

    # 비밀번호 재 설정(비밀번호 찾기 기능)
    def patch(self,request):
        # 재 설정 하고자하는 비밀번호가 기존 비밀번호와 일치할 경우
        owner = get_object_or_404(User,email = request.data['email'])
        if check_password(request.data['password'], owner.password):
            return Response({"message": "기존의 비밀번호로 변경할 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

        # 비밀번호가 올바른지 검증
        if True != validated.validated_password(request.data['password']):
            return Response({"message": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        if owner.auth_code == '':
            return Response({"message":"먼저 인증코드를 발급받아주세요."},status=status.HTTP_400_BAD_REQUEST)
        elif not owner.auth_code == request.data['auth_code']:
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_401_UNAUTHORIZED)

        serializer = UserSerializer(owner, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            owner.auth_code = ''
            owner.is_active = True
            owner.save()
            # 자신의 비밀 번호를 찾지 못할 때 비밀 번호 재 설정
            return Response({"message":"비밀번호를 재 설정 했습니다."}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserLikes(APIView):
    def get(self, request, challenge_id):
        try:
            challenge = get_object_or_404(Challenge, id=challenge_id)
        except AttributeError:
            return Response({"message": "게시글을 찾을 수 없습니다."}, status=status.HTTP_404_NOT_FOUND)
        serializer = GetCommentLikeUserInfo(challenge)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request,challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = get_object_or_404(User,id=request.user.id)
        if challenge in user.challenge_like.all():
            return Response({"message": "좋아요 목록에 등록되어 있습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message": "좋아요 목록에 등록되어 있지 않습니다."}, status=status.HTTP_204_NO_CONTENT)

    def patch(self, request,challenge_id):
        try :
            user = get_object_or_404(User,email = request.user.email)
        except AttributeError:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        try:
            challenge = get_object_or_404(Challenge,id=challenge_id)
        except AttributeError:
            return Response({"message": "챌린지 게시글이 존재하지 않습니다."}, status=status.HTTP_404_NOT_FOUND)

        if challenge in user.challenge_like.all():
            user.challenge_like.remove(challenge)
            return Response({"message":"좋아요 목록에 제거했습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            user.challenge_like.add(challenge)
            return Response({"message": "좋아요 목록에 추가하였습니다."}, status=status.HTTP_201_CREATED)



class UserBookMark(APIView):
    # 챌린지 게시글에 북마크 등록한 사람들의 정보 불러오기
    def get(self,request,challenge_id):
        challenge = get_object_or_404(Challenge,id=challenge_id)
        serializer = GetBookmarkUserInfo(challenge)
        return Response(serializer.data,status=status.HTTP_200_OK)

    def post(self, request,challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = get_object_or_404(User,id=request.user.id)
        if challenge in user.bookmark.all():
            return Response({"message": "북마크 목록에 등록되어 있습니다."}, status=status.HTTP_200_OK)
        else :
            return Response({"message": "북마크 목록에 등록되어 있지 않습니다."}, status=status.HTTP_204_NO_CONTENT)

    # 사용자가 북마크 등록, 등록 취소
    def patch(self, request,challenge_id):
        try:
            user = get_object_or_404(User, email=request.user.email)
        except AttributeError:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        challenge = get_object_or_404(Challenge,id=challenge_id)

        if challenge in user.bookmark.all():
            user.bookmark.remove(challenge)
            return Response({"message":"북마크 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            user.bookmark.add(challenge)
            return Response({"message": "북마크 등록 했습니다."}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer




############################ 소셜 로그인 ############################
# 각각의 get 메소드는 프론트에 api key를 전달하기 위한 메소드입니다.
# 각각의 post 메소드는 프론트에서 받은 데이터로 액세스 토큰과 유저 데이터를 받아와서 SocialLogin함수를 호출합니다.
# SocialLogin 함수는 해당 정보를 바탕으로 유저가 있다면 로그인하고, 없다면 유저를 생성합니다.
GOOGLE_API_KEY = os.environ.get("SGOOGLE_API_KEY")
class GoogleLogin(APIView):
    """구글 소셜 로그인"""

    GOOGLE_API_KEY = os.environ.get("SGOOGLE_API_KEY")
    def get(self, request):
        return Response(GOOGLE_API_KEY, status=status.HTTP_200_OK)

    def post(self, request):
        access_token = request.data["access_token"]
        user_data = requests.get(
            "https://www.googleapis.com/oauth2/v2/userinfo",
            headers={"Authorization": f"Bearer {access_token}"},
        )
        user_data = user_data.json()
        data = {
            "profile_image": user_data.get("picture"),
            "email": user_data.get("email"),
            "username": user_data.get("name"),
            "login_type": "google",
        }
        return SocialLogin(**data)


def SocialLogin(**kwargs):
    """소셜 로그인, 회원가입"""
    # 각각 소셜 로그인에서 email, username, login_type등을 받아옴!!
    data = {k: v for k, v in kwargs.items() if v is not None}
    # none인 값들은 빼줌
    email = data.get("email")
    login_type = data.get("login_type")
    # 그 중 email이 없으면 회원가입이 불가능하므로
    # 프론트에서 메시지를 띄워주고, 다시 로그인 페이지로 이동시키기
    if not email:
        return Response(
            {"error": "해당 계정에 email정보가 없습니다."}, status=status.HTTP_400_BAD_REQUEST
        )
    try:
        user = User.objects.get(email=email)
        # 로그인 타입까지 같으면, 토큰 발행해서 프론트로 보내주기
        if login_type == user.login_type:
            refresh = RefreshToken.for_user(user)
            access_token = CustomTokenObtainPairSerializer.get_token(user)
            return Response(
                {"refresh": str(refresh), "access": str(access_token.access_token)},
                status=status.HTTP_200_OK,
            )
        # 유저의 다른 소셜계정으로 로그인한 유저라면, 해당 로그인 타입을 보내줌.
        # (프론트에서 "{login_type}으로 로그인한 계정이 있습니다!" alert 띄워주기)
        else:
            return Response(
                {"error": f"{user.login_type}으로 이미 가입된 계정이 있습니다!"},
                status=status.HTTP_400_BAD_REQUEST,
            )
    # 유저가 존재하지 않는다면 회원가입시키기
    except User.DoesNotExist:
        new_user = User.objects.create(**data)
        # pw는 사용불가로 지정
        new_user.set_unusable_password()
        new_user.save()
        # 이후 토큰 발급해서 프론트로
        refresh = RefreshToken.for_user(new_user)
        access_token = CustomTokenObtainPairSerializer.get_token(new_user)
        return Response(
            {"refresh": str(refresh), "access": str(access_token.access_token)},
            status=status.HTTP_200_OK,
        )