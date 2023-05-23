from django.db import models
from django.conf import settings
from datetime import date

# Create your models here.

# 챌린지 feed
class Challenge(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)



# 소비경향 model
class ConsumeStyle(models.Model):
    style = models.CharField(max_length=32, verbose_name="소비경향")
    
    def __str__(self):
        return self.style



# 수입액 model
class Income(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    income_money = models.PositiveIntegerField(verbose_name="지출금액단가", default=0, blank=False)
    date = models.DateField("Date",default=date.today)



# 저축액 model
class Accountplus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Date",default=date.today)
    challenge = models.ForeignKey(Challenge, on_delete=models.PROTECT)
    plus_money = models.PositiveIntegerField(verbose_name="저축액", default=0, blank=False)
    


# 지출액 model
class Accountminus(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    date = models.DateField("Date",default=date.today)
    consumer_style = models.ManyToManyField("ConsumeStyle", verbose_name="소비경향", blank=False)
    
    amount = models.PositiveIntegerField(default=1, verbose_name="수량", blank=False)
    minus_money = models.PositiveIntegerField(verbose_name="지출금액단가", default=0, blank=False)
    placename = models.CharField(max_length=50, verbose_name="매장 이름", default="", blank=False)
    placewhere = models.CharField(max_length=70, verbose_name="매장주소", default="", blank=False)

    def __str__(self):
        return self.placename + str(self.minus_money*self.amount)



