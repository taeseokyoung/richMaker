from rest_framework import serializers
from articles.models import Accountminus, Accountplus, Income, ConsumeStyle, Challenge
from users.models import User


# 챌린지
class ChallengeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = [
            'challenge_title',
            'challenge_content',
            'amount',
            'period',
            # 'images',
            ]


class ChallengeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bookmarking_people_count',)
        
class ChallengeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('challenge_title', 'id', )


# 현재는 write와 동일하나 수정 시 제외되는 부분이 있었으면 합니다. (챌린지니까)
class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['challenge_title','challenge_content','amount','period','main_image','sub_image1','sub_image2','sub_image3']


class ChallengeListSerializer(serializers.ModelSerializer):
    user = serializers.SerializerMethodField()

    def get_user(self, obj):
        return obj.user.username

    class Meta:
        model = Challenge
        fields = [
            'id',
            'user',
            'challenge_title',
            'challenge_content',
            'amount',
            'period',
        ]


# 챌린지 멤버 카운트
class ChallengeMemberSerializer(serializers.ModelSerializer):
    bookmarking_people_count = serializers.SerializerMethodField()

    def get_bookmarking_people_count(self,obj):
        return obj.bookmarking_people.count()
    class Meta:
        model = User
        fields = ('bookmarking_people_count',)

# 소비경향
class ConsumerstyleSerializer(serializers.ModelSerializer):
    class Meta:
        model=ConsumeStyle
        fields = '__all__'
    
    def __str__(self):
        return self.style


# 수입액 작성, 보여주기, 수정하기
class IncomeSerializer(serializers.ModelSerializer):
    class Meta:
        model=Income
        exclude = ('user',)
    

# 지출액 작성, 자세히 보여주기, 수정하기
class AccountminusSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountminus
        exclude = ('user',)
        
    def get_totalminus(self, obj):
        return obj.minus_money*obj.amount
    

# 지출액 간단하게 보여주기(지출장소, 총금액)
class AccountminusShortSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountminus
        fields = ['date','placename','totalminus']
    
    def get_totalminus(self, obj):
        return obj.minus_money*obj.amount
        
        
# 저축액 작성, 수정하기
class AccountplusSerializer(serializers.ModelSerializer):
    
    class Meta:
        model=Accountplus
        exclude = ('user',)
