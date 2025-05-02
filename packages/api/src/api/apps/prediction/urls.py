from django.urls import URLPattern, URLResolver, path

from api.apps.prediction.views import PredictionAPIView

urlpatterns: list[URLResolver | URLPattern] = [
    path("", PredictionAPIView.as_view(), name="prediction"),
]
