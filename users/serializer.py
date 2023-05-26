from rest_framework import serializers
from users.models import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer


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

class GetBookmarkUserInfo(serializers.ModelSerializer):
    bookmarking_people = serializers.StringRelatedField(many=True)
    bookmarking_people_count = serializers.SerializerMethodField()

    def get_bookmarking_people_count(self,obj):
        return obj.bookmarking_people.count()
    class Meta:
        model = User
        fields = ('bookmarking_people','bookmarking_people_count')

class GetCommentLikeUserInfo(serializers.ModelSerializer):
    liking_people = serializers.StringRelatedField(many=True)
    liking_people_count = serializers.SerializerMethodField()

    def get_liking_people_count(self,obj):
        return obj.liking_people.count()
    class Meta:
        model = User
        fields = ('liking_people','liking_people_count')







# payload 재정의
class ComtomTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)
        token['email'] = user.email
        token['username'] = user.username
        return token
