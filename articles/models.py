from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.

# 챌린지 feed
class Challenge(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)


# 가계부지출 model
class Accountminus(models.Model):
    amount = models.PositiveIntegerField(default=1, verbose_name="수량", blank=False)
    minus_money = models.PositiveIntegerField(verbose_name="지출금액단가", default=0, blank=False)
    placename = models.CharField(max_length=50, verbose_name="매장 이름", default="", blank=False)
    placewhere = models.CharField(max_length=70, verbose_name="매장주소", default="", blank=False)

    def __str__(self):
        return self.placename + str(self.minus_money*self.amount)


# 가계부 feed
class Account(models.Model):
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    challenge = models.ForeignKey(Challenge, related_name="title", on_delete=models.PROTECT)
    
    # 정보
    date = models.DateField("Date",default=date.today)
    plus_money = models.PositiveIntegerField(verbose_name="저축액", default=0, blank=False)
    minus_info = models.ForeignKey(Accountminus, on_delete=models.CASCADE, related_name="money")
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    
    def __str__(self):
        return self.date
    

