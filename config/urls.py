from django.contrib import admin
from django.urls import include, path

admin.site.site_header = "HYPERSET admin"
admin.site.site_title = "HYPERSET admin"

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("tracker.urls")),
]
