from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from articles.serializers import (
    IncomeSerializer,
    AccountminusSerializer,
    AccountminusShortSerializer,
    AccountplusSerializer
    )
from articles.models import Income, Accountminus, Accountplus, ConsumeStyle, Challenge
from datetime import datetime

# Create your views here.

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

        