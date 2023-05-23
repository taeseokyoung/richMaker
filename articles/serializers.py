from rest_framework import serializers
from articles.models import Accountminus, Accountplus, Income, ConsumeStyle

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
        exclude = ['user',]
    

# 지출액 작성, 자세히 보여주기, 수정하기
class AccountminusSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountminus
        exclude = ['user',]
        
    def get_totalminus(self, obj):
        return sum(obj.minus_money*obj.amount)
    

# 지출액 간단하게 보여주기(지출장소, 총금액)
class AccountminusShortSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountminus
        fields = ['date','placename','totalminus']
    
    def get_totalminus(self, obj):
        return sum(obj.minus_money*obj.amount)
        
        
# 저축액 작성, 수정하기
class AccountplusSerializer(serializers.ModelSerializer):
    challenge = serializers.SerializerMethodField()
    
    class Meta:
        model=Accountplus
        exclude = ['user',]
        
    def get_challenge(self, obj):
        return self.challenge.title


