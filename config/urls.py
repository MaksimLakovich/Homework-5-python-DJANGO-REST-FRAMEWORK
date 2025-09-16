from typing import cast

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLResolver, include, path
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from rest_framework import permissions

schema_view = get_schema_view(
    openapi.Info(
        title="LMS API",
        default_version="v1",
        description="Документация к API LMS-платформы",
        contact=openapi.Contact(email="maks_lakovich@gmail.com"),
        license=openapi.License(name="BSD License"),
    ),
    public=True,
    permission_classes=(permissions.AllowAny,),
)

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1) namespace="users"
    # - это заданное пространство имен, которое есть в users/urls.py с помощью UsersConfig.name
    # 2) route:""
    # - ничего не указываю, так как DefaultRouter() из lms_system/urls.py создаст URL-ы (например, /api/lms/courses/)
    path("api/", include("users.urls", namespace="users")),
    path("api/", include("lms_system.urls", namespace="lms")),
    # URL-шаблоны для API документации:
    path(
        "swagger/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("redoc/", schema_view.with_ui("redoc", cache_timeout=0), name="schema-redoc"),
]

if settings.DEBUG:
    urlpatterns += cast(
        list[URLResolver], static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
