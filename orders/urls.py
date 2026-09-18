from django.urls import path

from .views import OrderPlacementView


urlpatterns = [
    path("", OrderPlacementView.as_view(), name="order-placement"),
]