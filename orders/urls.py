from django.urls import path

from .views import (
    BuyerOrderDetailView,
    BuyerOrderListView,
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
]