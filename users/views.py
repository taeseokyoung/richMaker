from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import ComtomTokenObtainPairSerializer,UserSerializer,ReadUserSerializer,GetBookmarkUserInfo,GetCommentLikeUserInfo
from .models import User
from . import validated
from articles.models import Challenge, Comment

class UserView(APIView):
    # 회원 정보 수정
    def put(self, request, user_id):
        if True != validated.validated_password(request.data['password']):
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        elif True != validated.validated_username(request.data['username']):
            return Response({"error": "유저네임이 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)
        owner = get_object_or_404(User, id=user_id)
        if request.user == owner:
            serializer = UserSerializer(owner,data=request.data,partial=True) # partial=True : 부분 업데이트
            if serializer.is_valid():
                serializer.save()
                update_user_info = ReadUserSerializer(owner)
                return Response(update_user_info.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({"error": "권한이 없습니다."}, status=status.HTTP_400_BAD_REQUEST)

    # 휴면 계정으로 전환
    def delete(self,request,user_id):
        owner = get_object_or_404(User,id=user_id)
        if request.user == owner:
            owner.is_active = False
            owner.save()
            return Response({"message": "휴면 계정으로 전환 되었습니다."}, status=status.HTTP_200_OK)
        else:
            return Response({"message":"권한이 없습니다."},status=status.HTTP_400_BAD_REQUEST)


class UserAPIView(APIView):
    # 이메일 발급 요청(비밀번호 찾기에 사용)
    def get(self,request):
        owner = get_object_or_404(User,email = request.data['email'])
        owner.auth_code = validated.send_email(owner.email)
        owner.save()
        return Response({"message": "인증 메일을 발송 했습니다."}, status=status.HTTP_200_OK)

    # 회원 가입
    def post(self,request):
        validated_result = validated.validated_data(request.data['email'],request.data['password'],request.data['username'])
        if validated_result != True:
            return Response({'message': validated_result}, status=status.HTTP_400_BAD_REQUEST)

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

    # 비밀번호 재 설정
    def patch(self,request):
        if True != validated.validated_password(request.data['password']):
            return Response({"error": "비밀번호가 올바르지 않습니다."}, status=status.HTTP_400_BAD_REQUEST)

        owner = get_object_or_404(User,email = request.data['email'])

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

            update_user_info = ReadUserSerializer(owner)
            # 자신의 비밀 번호를 찾지 못할 때 비밀 번호 재 설정
            return Response(update_user_info.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserLikes(APIView):
    # 댓글에 좋아요 누른 사람들의 정보 불러오기
    def get(self, request, comment_id):
        comment = get_object_or_404(Comment, id=comment_id)
        serializer = GetCommentLikeUserInfo(comment)
        return Response(serializer.data, status=status.HTTP_200_OK)

    # 사용자가 댓글을 좋아요, 좋아요 취소
    def post(self, request,comment_id):
        try :
            user = get_object_or_404(User,email = request.user.email)
        except AttributeError:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)

        comment = get_object_or_404(Comment,id=comment_id)
        # 해당 댓글 정보가 유저의 many to many 필드 데이터에 있다면 좋아요 취소
        if comment in user.comment_like.all():
            user.comment_like.remove(comment)
            return Response({"message":"like cancel"}, status=status.HTTP_204_NO_CONTENT)
        else:
            user.comment_like.add(comment)
            return Response({"message": "add cancel"}, status=status.HTTP_201_CREATED)

class UserBookMark(APIView):
    # 챌린지 게시글에 북마크 등록한 사람들의 정보 불러오기
    def get(self,request,challenge_id):
        challenge = get_object_or_404(Challenge,id=challenge_id)
        serializer = GetBookmarkUserInfo(challenge)
        return Response(serializer.data,status=status.HTTP_200_OK)

    # 사용자가 북마크 등록, 등록 취소
    def post(self, request,challenge_id):
        try:
            user = get_object_or_404(User, email=request.user.email)
        except AttributeError:
            return Response({"message": "로그인이 필요합니다."}, status=status.HTTP_401_UNAUTHORIZED)
        challenge = get_object_or_404(Challenge,id=challenge_id)

        if challenge in user.bookmark.all():
            user.bookmark.remove(challenge)
            return Response({"message":"bookmark cancel"}, status=status.HTTP_204_NO_CONTENT)
        else:
            user.bookmark.add(challenge)
            return Response({"message": "add bookmark"}, status=status.HTTP_201_CREATED)


class CustomTokenObtainPairView(TokenObtainPairView):
    serializer_class = ComtomTokenObtainPairSerializer