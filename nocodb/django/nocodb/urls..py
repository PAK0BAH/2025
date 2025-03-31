from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path("nocodb/", include("nocodb.urls")),
    path("admin/", admin.site.urls),
]