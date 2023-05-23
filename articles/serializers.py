from rest_framework import serializers
from .models import Challenge, ChallengeImage,Comment



class ChallengeSerializer(serializers.ModelSerializer):
    # images = serializers.ImageField(use_url=True)
    images = serializers.SerializerMethodField()
    
    def get_images(self, obj):
        image = obj.challengeimage_set.all()
        return ChallengeImageSerializer(instance=image, many=True).data
    
    class Meta:
        model = Challenge
        fields = ["id", "challenge_title", "challenge_content","amount", "period", "created_at", "updated_at", "images"]

    def create(self, validated_data):
        instance = Challenge.objects.create(**validated_data)
        image_set = self.context['request'].FILES
        for image_data in image_set.getlist('image'):
            ChallengeImage.objects.create(diary=instance, image=image_data)
        return instance


class ChallengeImageSerializer(serializers.ModelSerializer):
    image = serializers.ImageField(use_url=True)
    class Meta:
        model = ChallengeImage
        fields = ['image']