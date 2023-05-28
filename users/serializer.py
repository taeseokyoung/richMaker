from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from articles.models import Challenge

class ProfileUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('email','username','bio','profile_image','money','bookmark','challenge_like')
        extra_kwargs = {
            "email" : {"read_only": True},
        }

        
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = "__all__"
        extra_kwargs = {
            "password": {"write_only": True},
        }
        
    def create(self, validated_data):
        user = super().create(validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user

        # 회원 정보 수정, 오버라이딩
    def update(self, instance, validated_data):
        user = super().update(instance, validated_data)
        # 비밀번호 복호화
        user.set_password(user.password)
        user.save()
        return user
    
class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_image","username",'id')


class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ("profile_image","username",'id')


class GetBookmarkUserInfo(serializers.ModelSerializer):
    bookmarking_people = UserProfileSerializer(many=True)
    bookmarking_people_count = serializers.SerializerMethodField()
    def get_bookmarking_people_count(self,obj):
        return obj.bookmarking_people.count()
    class Meta:
        model = User
        fields = ('username', 'profile_image', 'bookmarking_people','bookmarking_people_count')


class GetCommentLikeUserInfo(serializers.ModelSerializer):
    liking_people =  UserProfileSerializer(many=True)
    liking_people_count = serializers.SerializerMethodField()
    def get_liking_people_count(self,obj):
        return obj.liking_people.count()
    class Meta:
        model = User
        fields = ('liking_people','liking_people_count',)


class ChallengeDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = Challenge
        exclude = ('created_at', 'updated_at')


class GetLikingChallengeSerializer(serializers.ModelSerializer):
    challenge_like = ChallengeDataSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('challenge_like',)

class GetBookingChallengeSerializer(serializers.ModelSerializer):
    bookmark = ChallengeDataSerializer(many=True,read_only=True)
    class Meta:
        model = User
        fields = ('bookmark',)



# payload 재정의
class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token

