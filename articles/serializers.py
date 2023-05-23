from rest_framework import serializers
from articles.models import Accountminus, Accountplus, Income, ConsumeStyle, Challenge, ChallengeImage
from users.models import User

# 챌린지
class ChallengeSerializer(serializers.ModelSerializer):
    # images = serializers.ImageField(use_url=True)
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        image = obj.challengeimage_set.all()
        return ChallengeImageSerializer(instance=image, many=True).data
    
    class Meta:
        model = Challenge
        fields = '__all__'

    def create(self, validated_data):
        instance = Challenge.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            ChallengeImage.objects.create(Challenge=instance, image=image_data)
        return instance

# 다중이미지
class ChallengeImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ChallengeImage
        fields = ['image']

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
    challenge_title = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountplus
        exclude = ('user',)
        
    def get_challenge_title(self, obj):
        return obj.challenge.challenge_title
