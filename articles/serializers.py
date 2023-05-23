from rest_framework import serializers
from articles.models import Challenge, Account, Accountminus


class AccountMinusSerializer(serializers.ModelSerializer):
    totalminus = serializers.SerializerMethodField()
    
    class Meta:
        model = Accountminus
        fields = '__all__'
        
    def get_totalminus(self, obj):
        return sum(obj.minus_money*obj.amount)


class AccountCreateSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Account
        exclude = ["author", "created_date", "updated_date"]


        
class AccountDetailSerializer(serializers.ModelSerializer):
    author = serializers.SerializerMethodField()
    challenge = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = '__all__'
        extra_kwargs = {'author' : {'read_only' : True},
                        'created_at' : {'read_only' : True},
                        'updated_at' : {'read_only' : True},
                        }
        
    def get_author(self, obj):
        return obj.author.username
    
    def get_challenge(self, obj):
        return obj.challenge.title
    

    
class AccountListSerializer(serializers.ModelSerializer):
    challenge = serializers.SerializerMethodField()
    
    class Meta:
        model = Account
        fields = ['challenge', 'minus_info', 'plus_money']
        
    def get_challenge(self, obj):
        return obj.challenge.title