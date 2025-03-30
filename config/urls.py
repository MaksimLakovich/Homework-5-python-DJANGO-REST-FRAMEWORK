from typing import cast

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLResolver, include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # 1) namespace="users"
    # - это заданное пространство имен, которое есть в users/urls.py с помощью UsersConfig.name
    # 2) route:""
    # - ничего не указываю, так как DefaultRouter() из lms_system/urls.py создаст URL-ы (например, /api/lms/courses/)
    path("", include("users.urls", namespace="users")),
    path("", include("lms_system.urls", namespace="lms")),
]

if settings.DEBUG:
    urlpatterns += cast(
        list[URLResolver], static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
