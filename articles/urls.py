from django.urls import path
from articles import views

urlpatterns = [
    # 수입 작성, 보기
    path('post/income/', views.IncomeView.as_view(), name="income_view"),
    # 수입 수정, 삭제
    path('post/income/<int:income_id>/', views.IncomeView.as_view(), name="income_update"),
    # 지출 작성
    path('post/minus/', views.AccountMinusView.as_view(), name="minus_view"),
    # 지출 자세히보기, 수정, 삭제
    path('post/minus/<int:minus_id>/', views.AccountMinusView.as_view(), name="minus_update"),
    # 지출 날짜별로 모아보기
    path('post/minus/<str:date>/', views.AccountShortView.as_view(), name="minus_date_view"),
    # 저축 작성
    path('post/plus/', views.AccountPlusView.as_view(), name="plus_view"),
    # 저축 수정, 삭제, 저축액 챌린지별로 보기
    path('post/plus/<int:plus_id>/', views.AccountPlusView.as_view(), name="plus_update"),
    # 챌린지 url
    path('challenge/', views.ChallengeView.as_view(), name='challenge_view'),
    path('challenge/post/', views.ChallengeWriteView.as_view(), name='challenge_post_view'),
    path('challenge/<int:challenge_id>/', views.ChallengeDatailView.as_view(), name='challenge_detail_view'),
]
