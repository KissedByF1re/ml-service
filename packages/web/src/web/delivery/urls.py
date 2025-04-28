from django.conf import settings
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.urls import URLPattern, URLResolver, re_path, path, include
from django.views.static import serve

urlpatterns: list[URLResolver | URLPattern] = [
    path("users/", include("web.apps.users.urls")),
    path("prediction/", include("web.apps.prediction.urls")),
    re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT}),
    re_path(r"^static/(?P<path>.*)$", serve, {"document_root": settings.STATIC_ROOT}),
]
urlpatterns += staticfiles_urlpatterns()
