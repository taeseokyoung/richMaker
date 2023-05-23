from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('sign-up/', views.UserAPIView.as_view(), name="sing_up"),
    # JWT Token 발급
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign-up/', views.UserAPIView.as_view(), name="sing_up"),
    #path('likes/<int:comment_id>/', views.UserLikes.as_view(), name="lieks"),
    path('bookmark/<int:challenge_id>/',views.UserBookMark.as_view(), name="bookmark"),
]
