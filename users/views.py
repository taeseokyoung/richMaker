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

    # 수입,지출 관리
    def fetch(self,request):
        pass



class UserAPIView(APIView):
    # 이메일 발급 요청(비밀번호 찾기에 사용)
    def get(self,request):
        try:
            owner = get_object_or_404(User,email = request.data['email'])
        except KeyError:
            return Response({"message": "요청하신 이메일을 찾을 수 없습니다."}, status=status.HTTP_400_BAD_REQUEST)
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

    # 이메일 인증 , 비밀번호 찾기
    def put(self,request):
        owner = get_object_or_404(User,email = request.data['email'])
        print(owner.auth_code)
        if owner.auth_code == '':
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_400_BAD_REQUEST)
        elif not owner.auth_code == request.data['auth_code']:
            return Response({"message":"인증 코드가 올바르지 않습니다."},status=status.HTTP_401_UNAUTHORIZED)
        try:
            serializer = UserSerializer(owner, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                update_user_info = ReadUserSerializer(owner)
                # 자신의 비밀 번호를 찾지 못할 때 비밀 번호 재 설정
                return Response(update_user_info.data,status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
        except KeyError: # Key Error , request에 password가 없을때 = > 사용자가 이메일 인증코드 발급만 요청했을 경우
            pass         # Key Error 가 발생하지 않을때 = > 사용자가 비밀번호 재 설정을 요청했을 경우

        owner.auth_code = ''
        owner.is_active = True
        owner.save()
        # 인증 메일 요청
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