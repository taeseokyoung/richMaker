from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.
class Challenge(models.Model):
    user = models.ForeignKey('users.User', on_delete=models.CASCADE)
    challenge_title = models.CharField("챌린지명", max_length=50)
    challenge_content = models.TextField("내용")
    amount = models.IntegerField("목표 금액")
    period = models.IntegerField("목표 기간")
    created_at = models.DateTimeField("생성 시간", auto_now_add=True)
    updated_at = models.DateTimeField("수정 시간", auto_now=True)
    main_image = models.ImageField(upload_to='challenge', default='media/no_image.jpg')
    
    def __str__(self):
        return self.challenge_title

# 소비경향 model
class ConsumeStyle(models.Model):
    style = models.CharField(max_length=32, verbose_name="소비경향")
    
    def __str__(self):
        return self.style


# 수입액 model
class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    income_money = models.PositiveIntegerField(verbose_name="수입", null=False, blank=False)
    date = models.DateField("Date",default=date.today)



# 저축액 model
class Accountplus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Date",default=date.today)
    challenge = models.ManyToManyField("Challenge", verbose_name="챌린지", blank=False)
    plus_money = models.PositiveIntegerField(verbose_name="저축액", null=False, blank=False)
    
    def __str__(self):
        return self.challenge.challenge_title + str(self.plus_money)
    


# 지출액 model
class Accountminus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Date",default=date.today)
    consumer_style = models.ManyToManyField("ConsumeStyle", verbose_name="소비경향", blank=False)
    
    amount = models.PositiveIntegerField(default=1, verbose_name="수량", blank=False)
    minus_money = models.PositiveIntegerField(verbose_name="지출금액단가", null=False, blank=False)
    placename = models.CharField(max_length=50, verbose_name="매장 이름", null=False, blank=False)
    placewhere = models.CharField(max_length=70, verbose_name="매장주소", null=False, blank=False)

    def __str__(self):
        return self.placename + str(self.minus_money*self.amount)

      
class Comment(models.Model):
    comment_title = models.TextField(default="Comment")

