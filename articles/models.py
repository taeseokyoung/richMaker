from django.db import models

# Create your models here.


class Challenge(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    challenge_title = models.CharField("챌린지명", max_length=50)
    challenge_content = models.TextField("내용")
    amount = models.IntegerField("목표 금액")
    period = models.CharField("목표 기간", max_length=10)
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)

    
class ChallengeImage(models.Model):
    challenge = models.ForeignKey(Challenge, on_delete=models.CASCADE)
    image = models.ImageField(default='media/no_image.jpg', upload_to = 'challenge', blank=True, null=True)