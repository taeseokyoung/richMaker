from django.urls import path
from articles import views

urlpatterns = [
    path('challenge/', views.ChallengeView.as_view(), name='challenge_view'),
    path('challenge/post', views.ChallengeWriteView.as_view(), name='challenge_post_view'),
    path('challenge/<int:challenge_id>', views.ChallengeDatailView.as_view(), name='challenge_detail_view'),
    path('<int:challenge_id>/bookmark', views.ChallengeBookmarkView.as_view(), name='challenge_detail_view'),
    path('<int:challenge_id>/member', views.ChallengeMemberView.as_view(), name='challenge_detail_view'),
]
