from django.db import models

# Create your models here.

class Challenge(models.Model):
    challenge_title = models.TextField(default="Challenge")
class Account(models.Model):
    account_title = models.TextField(default="Account")
class Comment(models.Model):
    comment_title = models.TextField(default="Comment")