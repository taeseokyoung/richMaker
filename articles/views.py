from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from articles.serializers import (
    IncomeSerializer,
    AccountminusSerializer,
    AccountminusShortSerializer,
    AccountplusSerializer,
    ChallengeSerializer, 
    ChallengeImageSerializer
    )
from articles.models import Income, Accountminus, Accountplus, ConsumeStyle, Challenge
from datetime import datetime

# Create your views here.

class ChallengeView(APIView):
    def get(self, request):
        '''
        챌린지 보기
        '''
        challenge = Challenge.objects.all()
        serializer = ChallengeSerializer(challenge, many=True)
        return Response(serializer.data)


class ChallengeWriteView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    def post(self,request):
        '''
        챌린지 쓰기
        '''
        serializer = ChallengeSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save(user=request.user)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class ChallengeDatailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def put(self, request, challenge_id):
        '''
        챌린지 수정하기
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.user == challenge.user:
            serializer = ChallengeSerializer(challenge, data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response(serializer.data, status=status.HTTP_200_OK)
            else:
                return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response("챌린지 수정 권한은 챌린지를 만든 사람에게 있습니다.", status=status.HTTP_403_FORBIDDEN)
    
    def delete(self, request, challenge_id):
        '''
        챌린지 삭제하기 : 챌린지를 시작한 사람이 없을 때
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.user == challenge.user:
            
            return Response({"message":"delete!"})


# 수입 views
class IncomeView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = IncomeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def get(self, request):
        income = Income.objects.filter(user=request.user)
        
        if income.user != request.user:
            return Response({"error":"작성자만이 확인할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = IncomeSerializer(income, data=request.data)
        
        serializer = IncomeSerializer(income)
        return Response(serializer.data, status=status.HTTP_200_OK)
        
        
    def put(self, request, income_id):
        income = get_object_or_404(Income, id=income_id)
        
        if income.user != request.user:
            return Response({"error":"작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = IncomeSerializer(income, data=request.data)
        
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, income_id):
        income = get_object_or_404(Income, id=income_id)
        
        if income.user != request.user:
            return Response({"error":"작성자만이 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        income.delete()
        return Response({"message": "삭제되었습니다."}, status.HTTP_204_NO_CONTENT)


# 지출 views
class AccountMinusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AccountminusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
        
    # 지출내역 자세히보기
    def get(self, request, minus_id):
        minus = get_object_or_404(Accountminus, id=minus_id)
        
        if minus.user != request.user:
            return Response({"error":"작성자만이 확인할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccountminusSerializer(minus)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, minus_id):
        minus = get_object_or_404(Accountminus, id=minus_id)
        
        if minus.user != request.user:
            return Response({"error":"작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccountminusSerializer(minus, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, minus_id):
        minus = get_object_or_404(Accountminus, id=minus_id)
        
        if minus.user != request.user:
            return Response({"error":"작성자만이 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        minus.delete()
        return Response({"message": "삭제되었습니다."}, status.HTTP_204_NO_CONTENT)



# 지출내역 날짜별로 모아서 보기 (이때는.. 요약해서 보기)
class AccountShortView(APIView):
    permission_classes = [IsAuthenticated]
    
    def get(self, request, date):
        try:
            parsed_date = datetime.strptime(date,'%Y-%m-%d')
        except ValueError:
            return Response({"잘못된 형식입니다."}, status=status.HTTP_404_NOT_FOUND)
            
        minus = Accountminus.objects.filter(date=parsed_date, user=request.user)
        
        if minus.user != request.user:
            return Response({"error":"작성자만이 확인할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccountminusShortSerializer(minus)
        return Response(serializer.data, status=status.HTTP_200_OK)
    


# 저축 views
class AccountPlusView(APIView):
    permission_classes = [IsAuthenticated]
    
    def post(self, request):
        serializer = AccountplusSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 챌린지 별 저축액 모아보기
    def get(self, request, challenge_id):
        plus = Accountplus.objects.filter(challenge_id=challenge_id, user=request.user)
        
        serializer = AccountplusSerializer(plus)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def put(self, request, plus_id):
        plus = get_object_or_404(Accountplus, id=plus_id)
        
        if plus.user != request.user:
            return Response({"error":"작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccountminusSerializer(plus, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, plus_id):
        plus = get_object_or_404(Accountminus, id=plus_id)
        
        if plus.user != request.user:
            return Response({"error":"작성자만이 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        plus.delete()
        return Response({"message": "삭제되었습니다."}, status.HTTP_204_NO_CONTENT)

        


