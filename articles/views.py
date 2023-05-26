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
    ConsumerstyleSerializer,
    ChallengeSerializer, 
    ChallengeMemberSerializer,
    ChallengeListSerializer,
    ChallengeUserSerializer,
    )
from articles.models import Income, Accountminus, Accountplus, ConsumeStyle, Challenge
from datetime import datetime
from django.utils import timezone
from articles.pagination import ChallengePagination
from users.models import User
from ai.main import AiCheck
import json
from django.db.models import Sum

# Create your views here.

class ChallengeView(APIView):
    permission_classes = [permissions.IsAuthenticated]
    
    def get(self, request):
        '''
        각 유저별 북마크한 챌린지 api
        '''
        user = get_object_or_404(User, id=request.user.id)
        bookmark_user = user.bookmark.all()
        print(bookmark_user)
        serializer = ChallengeUserSerializer(bookmark_user, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    def post(self,request):
        '''
        챌린지 쓰기
        '''
        serializer = ChallengeSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response (serializer.errors)

class ChallengeDetailView(APIView):
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    def put(self, request, challenge_id):
        '''
        챌린지 수정하기
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        if request.user.id == challenge.user_id:
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
        챌린지 삭제하기 : 챌린지를 시작한 사람이 없을 때만
        '''
        challenge = get_object_or_404(Challenge, id=challenge_id)
        serializer = ChallengeMemberSerializer(challenge)
        challengeMember = serializer.data.get('bookmarking_people_count')
        if challengeMember == 0:
            if request.user.id == challenge.user_id:
                challenge.delete()
                return Response("챌린지가 삭제되었습니다.", status=status.HTTP_204_NO_CONTENT)
            else:
                return Response("챌린지 삭제 권한이 없습니다.", status=status.HTTP_403_FORBIDDEN)
        else:
            return Response("챌린지를 삭제할 수 없습니다.", status=status.HTTP_403_FORBIDDEN)


class ChallengeListView(APIView):
    """
    신규 챌린지 별, 상위 챌린지 별 (추후 소비 통계 관련 데이터 포함)
    """
    pagination_class = ChallengePagination
    serializer_class = ChallengeListSerializer
    @property
    def paginator(self):
        if not hasattr(self, '_paginator'):
            if self.pagination_class is None:
                self._paginator = None
            else:
                self._paginator = self.pagination_class()
        else:
            pass
        return self._paginator

    def paginate_queryset(self, queryset):

        if self.paginator is None:
            return None
        return self.paginator.paginate_queryset(queryset,
                   self.request, view=self)

    def get_paginated_response(self, data):
        assert self.paginator is not None
        return self.paginator.get_paginated_response(data)

    def get(self, request):
        if request.GET.get('query') == None:
            current_time = timezone.now()
            # 이달의 신규 챌린지
            new_challenge_of_month = Challenge.objects.filter(created_at__range=(current_time - timezone.timedelta(days=30),current_time))
            new_challenge_count = new_challenge_of_month.count()
            new_challenge_serializer = ChallengeListSerializer(new_challenge_of_month, many=True)
            # 북마크 상위 챌린지
            top_challenge = Challenge.objects.annotate(total_sum=Sum('bookmarking_people')).order_by('-total_sum')
            top_challenge_serializer = ChallengeListSerializer(top_challenge[:5], many=True)

            return Response({"new_challenge": {"count": new_challenge_count, "list": new_challenge_serializer.data}, "top_challenge": {"list": top_challenge_serializer.data}}, status=status.HTTP_200_OK)

        elif request.GET.get('query') == 'top':
            # 일단 높은 순. 추후 수정 필요
            top_challenge = Challenge.objects.annotate(total_sum=Sum('bookmarking_people')).order_by('-total_sum')
            page = self.paginate_queryset(top_challenge)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(new_challenge, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.GET.get('query') == 'new':
            new_challenge = Challenge.objects.all().order_by('-created_at')
            page = self.paginate_queryset(new_challenge)
            if page is not None:
                serializer = self.get_paginated_response(self.serializer_class(page, many=True).data)
            else:
                serializer = self.serializer_class(new_challenge, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

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

    # 날짜별 수입보기
    def get(self, request, date):
        income = Income.objects.filter(user_id=request.user.id, date=date)
        # print(request.user.id)
        serializer = IncomeSerializer(income, many=True)
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
        print(request.data)
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
            
        minus = Accountminus.objects.filter(date=parsed_date, user_id=request.user.id)
        
        serializer = AccountminusShortSerializer(minus, many=True)
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
            
    # 날짜별 저축액 모아보기
    def get(self, request, date):
        plus = Accountplus.objects.filter(date=date, user=request.user)
        
        serializer = AccountplusSerializer(plus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
            
    
class AccountPlusDetailView(APIView):
    permission_classes = [IsAuthenticated]
     
    # 챌린지별 저축액 모아보기
    def get(self, request, plus_id):
        plus = Accountplus.objects.filter(challenge_id=plus_id, user=request.user)
        
        serializer = AccountplusSerializer(plus, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    
    
    def put(self, request, plus_id):
        plus = get_object_or_404(Accountplus, id=plus_id)
        
        if plus.user != request.user:
            return Response({"error":"작성자만이 수정할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        serializer = AccountplusSerializer(plus, data=request.data)
        if serializer.is_valid():
            serializer.save(user=request.user)
            return Response(serializer.data)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


    def delete(self, request, plus_id):
        plus = get_object_or_404(Accountplus, id=plus_id)
        
        if plus.user != request.user:
            return Response({"error":"작성자만이 삭제할 수 있습니다."}, status=status.HTTP_403_FORBIDDEN)

        plus.delete()
        return Response({"message": "삭제되었습니다."}, status.HTTP_204_NO_CONTENT)

        

# 소비경향 view
class ConsumerStyleView(APIView):
    def get(self, request):
        style = ConsumeStyle.objects.all()
        serializer = ConsumerstyleSerializer(style, many=True)
        return Response(serializer.data)
    

# AI 영수증 체크
class AiCheckView(APIView):
    def post(self, request):
        ai_data = json.dumps(AiCheck(request.data['base64String']))
        return Response(ai_data, status=status.HTTP_200_OK)