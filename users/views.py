from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.generics import get_object_or_404
from .models import User
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializer import ComtomTokenObtainPairSerializer,UserSerializer,ReadUserSerializer
from . import validated


class UserView(APIView):
    # 회원 정보 수정
    def put(self, request, user_id):
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

    # 수입,지출 관리
    def fetch(self,request):
        pass

class ProfileView(APIView):
    # 프로필 정보 읽기
    def get(self,request):
        pass
    # 프로필 정보 수정
    def put(self,request):
        pass


class UserAPIView(APIView):
    # 회원 가입
    def post(self,request):
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

    def put(self,request):
        owner = get_object_or_404(User,email = request.data['email'])

        if owner.auth_code == '':
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_400_BAD_REQUEST)
        if not owner.auth_code == request.data['auth_code']:
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_401_UNAUTHORIZED)

        owner.auth_code = ''
        owner.is_active = True
        owner.save()
        return Response({"message":"인증 되었습니다."},status=status.HTTP_200_OK)



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