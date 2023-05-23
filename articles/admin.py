from django.contrib import admin
from .models import Challenge, Accountminus, Accountplus, Income, ConsumeStyle,Comment
# Register your models here.
admin.site.register(Challenge)
admin.site.register(Accountminus)
admin.site.register(Accountplus)
admin.site.register(Income)
admin.site.register(ConsumeStyle)
admin.site.register(Comment)