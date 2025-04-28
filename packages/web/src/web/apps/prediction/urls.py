from django.urls import URLResolver, URLPattern, path

from web.apps.prediction.views import PredictionView

urlpatterns: list[URLResolver | URLPattern] = [
    path("", PredictionView.as_view(), name="prediction"),
]
