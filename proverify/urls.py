from django.contrib import admin
from django.urls import path, include
from django.shortcuts import redirect
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView

from codes.views import (
    admin_login_page,
    admin_dashboard_page,
    admin_upload_page,
    admin_codes_page,
    admin_details_page,
    verify_page,
)

urlpatterns = [
    # Root redirect -> verify page (public-facing)
    path("", lambda request: redirect("/verify/"), name="home"),

    # Django built-in admin
    path("django-admin/", admin.site.urls),

    # Frontend pages served by Django
    path("admin-login/", admin_login_page, name="admin-login"),
    path("admin-dashboard/", admin_dashboard_page, name="admin-dashboard"),
    path("admin-upload/", admin_upload_page, name="admin-upload"),
    path("admin-codes/", admin_codes_page, name="admin-codes"),
    path("admin-details/", admin_details_page, name="admin-details"),
    path("verify/", verify_page, name="verify"),

    # REST API
    path("api/auth/login/", TokenObtainPairView.as_view()),
    path("api/auth/refresh/", TokenRefreshView.as_view()),
    path("api/", include("codes.urls")),
]
