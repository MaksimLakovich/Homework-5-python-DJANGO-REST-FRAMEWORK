from typing import cast

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import URLResolver, include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    # namespace="users" это заданное пространство имен, которое есть в users/urls.py с помощью UsersConfig.name
    path("api/users/", include("users.urls", namespace="users")),
    path("api/lms/", include("lms_system.urls", namespace="lms")),
]

if settings.DEBUG:
    urlpatterns += cast(
        list[URLResolver], static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    )
