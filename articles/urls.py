from django.urls import path
from articles import views

urlpatterns = [
    # 가계부 작성
    path('post/', views.AccountView.as_view(), name="account_create"),
    # 챌린지별 해당 날짜에 대한 가계부 모두 불러오기
    path('post/<int:challenge_id>/', views.AccountView.as_view(), name="account_list"),
    # 가계부 자세히보기
    path('post/<int:challenge_id>/<int:account_id>/', views.AccountDetailView.as_view(), name="account_detailview"),
    # 수정, 삭제
    path('post/<int:account_id>/', views.AccountDetailView.as_view(), name="account_update"),
]
