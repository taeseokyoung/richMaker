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


class GetLikingChallenge(APIView):
    """ 사용자가 좋아요 등록한 챌린지 목록 뽑아오기 """
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer = GetLikingChallengeSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

class GetBookingChallenge(APIView):
    """ 사용자가 (북마크 등록) 챌린지 참여 목록 뽑아오기 """
    def get(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        serializer = GetBookingChallengeSerializer(owner)
        return Response(serializer.data,status=status.HTTP_200_OK)

class UserProfile(APIView):
    """ 사용자가 (북마크 등록) 챌린지 참여 목록 뽑아오기 """
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
        return Response(serializer.data ,status=status.HTTP_200_OK)
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

# 이메일 발급 요청(비밀번호 찾기에 사용)
class GetAuthTokenAPIView(APIView):
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
    """북마크 조회, 사용자 북마크 등록 여부 확인 ,등록 및 취소,"""
    # 챌린지에 북마크 등록한 유저 정보 뽑아오기
    def get(self,request,challenge_id):
        challenge = get_object_or_404(Challenge,id=challenge_id)
        serializer = GetBookmarkUserInfo(challenge)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 사용자가 챌린지에 북마크 등록 되어잇는지 판단
    def post(self, request,challenge_id):
        challenge = get_object_or_404(Challenge, id=challenge_id)
        user = get_object_or_404(User,id=request.user.id)
        if challenge in user.bookmark.all():
            return Response({"message": "북마크 목록에 등록되어 있습니다."}, status=status.HTTP_200_OK)
        else :
            return Response({"message": "북마크 목록에 등록되어 있지 않습니다."}, status=status.HTTP_204_NO_CONTENT)

    # 사용자가 북마크 등록, 등록 취소
    def patch(self, request,challenge_id):
        user = get_object_or_404(User, email=request.user.email)
        challenge = get_object_or_404(Challenge,id=challenge_id)
        if challenge in user.bookmark.all():
            user.bookmark.remove(challenge)
            return Response({"message":"북마크 취소했습니다."}, status=status.HTTP_204_NO_CONTENT)
        else:
            user.bookmark.add(challenge)
            return Response({"message": "북마크 등록 했습니다."}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer







