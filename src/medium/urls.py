from dj_rest_auth.views import PasswordResetConfirmView
from django.conf import settings
from django.contrib import admin
from django.urls import include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="Medium Clone API",
        default_version="v1",
        description="API endpoints for Medium API Course",
        contact=openapi.Contact(email="support@kosamtech.com"),
        license=openapi.License(name="MIT License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

API_VERSION = "api/v1"

urlpatterns = [
    path(settings.ADMIN_URL, admin.site.urls),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0)),
    path(
        f"{API_VERSION}/auth/password/reset/confirm/<uid64>/<token>",
        PasswordResetConfirmView.as_view(),
        name="password_reset_confirm",
    ),
    path(f"{API_VERSION}/auth/user/", include("users.urls")),
    path(
        f"{API_VERSION}/auth/registration/", include("dj_rest_auth.registration.urls")
    ),
    path(f"{API_VERSION}/auth/", include("dj_rest_auth.urls")),
    path(f"{API_VERSION}/profiles/", include("profiles.urls")),
]

admin.site.site_header = "Medium API Admin"
admin.site.site_title = "Medium API Admin Portal"
admin.site.index_title = "Welcome to Medium API Portal"
