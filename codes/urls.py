from django.urls import path
from .views import (
    UploadCodesAPIView,
    VerifyCodeAPIView,
    ProductCodeListAPIView,
    CodeBatchListAPIView,
    DashboardStatsAPIView,
    EmailLoginAPIView,
)

urlpatterns = [
    path('codes/upload/', UploadCodesAPIView.as_view(), name='upload-codes'),
    path('verify/', VerifyCodeAPIView.as_view(), name='verify-code'),
    path('codes/', ProductCodeListAPIView.as_view(), name='list-codes'),
    path('batches/', CodeBatchListAPIView.as_view(), name='list-batches'),
    path('dashboard/stats/', DashboardStatsAPIView.as_view(), name='dashboard-stats'),
    path('auth/email-login/', EmailLoginAPIView.as_view(), name='email-login'),
]
