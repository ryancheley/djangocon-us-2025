from django.urls import path

from .views import HealthCheckView

app_name = "accounts"

urlpatterns = [
    path("", HealthCheckView.as_view(), name="health-check"),
]
