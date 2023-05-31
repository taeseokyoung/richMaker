from rest_framework import serializers
from articles.models import Accountminus, Accountplus, Income, ConsumeStyle, Challenge, Comment
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
            'main_image',
            ]


class ChallengeWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('bookmarking_people_count',)
        
class ChallengeUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ('challenge_title', 'id', 'user')


# 현재는 write와 동일하나 수정 시 제외되는 부분이 있었으면 합니다. (챌린지니까)
class ChallengeDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        fields = ['id','challenge_title','challenge_content','amount','period','main_image']


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
            'main_image'
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
    stylename= serializers.SerializerMethodField()
    
    class Meta:
        model=Accountminus
        fields = [
                'date',
                'consumer_style',
                'amount',
                'minus_money',
                'placename',
                'placewhere',
                'totalminus',
                'stylename',
                ]
        
    def get_totalminus(self, obj):
        return obj.minus_money*obj.amount
    
    def get_stylename(self, obj):
        return obj.consumer_style.style
    

# 지출액 간단하게 보여주기(지출장소, 총금액)
# class AccountminusShortSerializer(serializers.ModelSerializer):
#     totalminus = serializers.SerializerMethodField()
    
#     class Meta:
#         model=Accountminus
#         fields = ['date','placename','totalminus']
    
#     def get_totalminus(self, obj):
#         return obj.minus_money*obj.amount
        
        
# 저축액 작성, 수정하기
class AccountplusSerializer(serializers.ModelSerializer):
    challenge_title = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountplus
        exclude = ('user',)
        
    def get_challenge_title(self, obj):
        return obj.challenge.challenge_title
        
# 지출액 자세히 보여주기
class AccountminusDetailSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    stylename= serializers.SerializerMethodField()
    class Meta:
        model=Accountminus
        fields = [
                'id',
                'date',
                'consumer_style',
                'amount',
                'minus_money',
                'placename',
                'placewhere',
                'totalminus',
                'stylename',
                ]
    def get_totalminus(self, obj):
        return obj.minus_money*obj.amount
    def get_stylename(self, obj):
        return obj.consumer_style.style
        
        
# 저축액 작성, 수정하기
class AccountplusSerializer(serializers.ModelSerializer):
    challenge_title = serializers.SerializerMethodField()

    class Meta:
        model=Accountplus
        exclude = ('user',)
        
    def get_challenge_title(self, obj):
        return obj.challenge.challenge_title
        
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_image","username",'id')

class CommentSerializer(serializers.ModelSerializer):
    owner_name = serializers.SerializerMethodField()
    owner_image = serializers.SerializerMethodField()
    def get_owner_name(self, obj):
        return obj.owner.username

    def get_owner_image(self, obj):
        return obj.owner.profile_image.url if obj.owner.profile_image else None
    class Meta:
        model = Comment
        exclude = ("created_at",)


class CommentCreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ("comment",)