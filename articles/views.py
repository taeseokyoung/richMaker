from rest_framework.views import APIView
from articles.models import Account
from articles.serializers import (
    AccountCreateSerializer, 
    AccountDetailSerializer, 
    AccountListSerializer,
    )
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import get_object_or_404
from rest_framework.permissions import IsAuthenticated

# Create your views here.
class AccountView(APIView):
    permission_classes = [IsAuthenticated]
    # 가계부 작성
    def post(self, request):
        serializer = AccountCreateSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(author = request.user)
            return Response(serializer.data, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
    # 챌린지별 가계부 불러오기 (placename, 총지출내역, 저축금액만 나옴)
    def get(self, request, challenge_id):
        account = Account.objects.filter(challenge_id=challenge_id)
        serializer = AccountListSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)


class AccountDetailView(APIView):
    permission_classes = [IsAuthenticated]
    
    # 가계부 자세히 불러오기
    def get(self, request, challenge_id, account_id):
        account = get_object_or_404(Account, challenge_id=challenge_id, id=account_id)
        serializer = AccountDetailSerializer(account)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    # 수정하기
    def put(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        
        if account.author != request.user:
            return Response({"error":"가계부의 작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        serializer = AccountCreateSerializer(account, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        
    # 삭제하기
    def delete(self, request, account_id):
        account = get_object_or_404(Account, id=account_id)
        
        if account.author !=  request.user:
            return Response({"error":"가계부의 작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)
        
        account.delete()
        return Response({"message": "삭제되었습니다."}, status.HTTP_204_NO_CONTENT)

    
    


        

    
    

    