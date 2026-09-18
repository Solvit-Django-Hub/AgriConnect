from django.urls import path

from .views import (
    FarmerOrderListView,
    FarmerOrderStatusUpdateView,
    OrderPlacementView,
)


urlpatterns = [
    path("", OrderPlacementView.as_view(), name="order-placement"),
    path(
        "farmer/",
        FarmerOrderListView.as_view(),
        name="farmer-order-list",
    ),
    path(
        "farmer/<int:order_id>/",
        FarmerOrderStatusUpdateView.as_view(),
        name="farmer-order-status-update",
    ),
]