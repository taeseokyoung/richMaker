from django.urls import path
from articles import views

urlpatterns = [
    path('challenge/', views.ChallengeView.as_view(), name='challenge_view'),
    path('challenge/post', views.ChallengeWriteView.as_view(), name='challenge_post_view'),
]
