from django.urls import path

from .views import BuyerProductDetailView, BuyerProductListView


urlpatterns = [
    path(
        "products/",
        BuyerProductListView.as_view(),
        name="buyer-product-list",
    ),
    path(
        "products/<int:product_id>/",
        BuyerProductDetailView.as_view(),
        name="buyer-product-detail",
    ),
]