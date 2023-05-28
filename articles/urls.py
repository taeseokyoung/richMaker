from django.urls import path
from articles import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    # 소비경향보기
    path('post/style/', views.ConsumerStyleView.as_view(), name="consumerstyle_view"),
    # 수입 작성 
    path('post/income/', views.IncomeView.as_view(), name="income_view"),
    # 날짜별로 수입 보기, 수입 수정, 삭제
    path('post/income/<str:date>/', views.IncomeView.as_view(), name="income_view"),
    # 지출 작성
    path('post/minus/', views.AccountMinusView.as_view(), name="minus_view"),
    # 지출 수정, 삭제, 하나의 지출 정보 가져오기
    path('post/minus/<int:minus_id>/', views.AccountMinusView.as_view(), name="minus_update"),
    # 지출 날짜별로 보기
    path('post/minus/<str:date>/', views.AccountShortView.as_view(), name="minus_date_view"),
    # 저축 작성
    path('post/plus/', views.AccountPlusView.as_view(), name="plus_view"),
    # 저축 수정, 삭제
    path('post/plus/<int:challenge_id>/<str:date>/', views.AccountUpdateView.as_view(), name="plus_update_view"),
    # 저축 챌린지별 저축 보기
    path('post/plus/<int:plus_id>/', views.AccountPlusDetailView.as_view(), name="plus_update"),
    # 저축액 날짜별로 보기
    path('post/plus/<str:date>/', views.AccountPlusView.as_view(), name="plus_date_view"),
    # 챌린지 url
    path('challenge/', views.ChallengeView.as_view(), name='challenge_view'),
    path('challenge/<int:challenge_id>/', views.ChallengeDetailView.as_view(), name='challenge_detail_view'),
     # 상세 API
    path('challenge/list', views.ChallengeListView.as_view(), name='challenge_list_view'),
    # AI 영수증 체크
    path('post/ai/', views.AiCheckView.as_view(), name='ai_check_view'),
]

urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)