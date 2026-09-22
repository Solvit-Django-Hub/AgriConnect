from django.urls import path

from .views import (
    BuyerOrderDetailView,
    BuyerOrderListView,
    FarmerOrderListView,
    FarmerOrderStatusUpdateView,
    OrderPlacementView,
)


urlpatterns = [
    path(
        "",
        OrderPlacementView.as_view(),
        name="order-placement",
    ),
    path(
        "my-orders/",
        BuyerOrderListView.as_view(),
        name="buyer-order-list",
    ),
    path(
        "my-orders/<int:order_id>/",
        BuyerOrderDetailView.as_view(),
        name="buyer-order-detail",
    ),
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
