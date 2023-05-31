from django.urls import path
from . import views,social
from rest_framework_simplejwt.views import TokenRefreshView



urlpatterns = [
    path('<int:user_id>/', views.UserView.as_view(), name='user_view'),
    path('sign-up/', views.UserAPIView.as_view(), name="sing_up"),
    path('get-auth-token/', views.GetAuthTokenAPIView.as_view(), name="get_auth_token"),
    # JWT Token 발급
    path('login/', views.CustomTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('sign-up/', views.UserAPIView.as_view(), name="sing_up"),
    path('likes/<int:challenge_id>/', views.UserLikes.as_view(), name="lieks"),
    path('bookmark/<int:challenge_id>/', views.UserBookMark.as_view(), name="bookmark"),
    path('profile/<int:user_id>/', views.UserProfile.as_view(), name="profile"),
    path('get-bookmarking-challenge/<int:user_id>/',views.GetBookingChallenge.as_view(),name="get-bookmarking-challenge"),
    path('get-liking-challenge/<int:user_id>/',views.GetLikingChallenge.as_view(),name="get-liking-challenge"),

    # 페이스북 로그인
    # path("facebook/callback/",social.FaceBookAPI.as_view(), name="facebook_API"),
    # 구글 로그인
    # path("google/callback/",social.GoogleAPI.as_view(), name="google_API"),
    # 카카오 로그인
    path("Kakao-login/",social.KakaoLogin.as_view(), name="kakao_API"),
]

