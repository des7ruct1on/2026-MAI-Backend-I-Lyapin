from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("admin/", admin.site.urls),
    path("web/", include("main.web_urls")),
    path("api/", include("main.api_urls")),
]
