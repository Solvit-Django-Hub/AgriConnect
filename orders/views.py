from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import Prefetch
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from farmers.models import Product

from .models import Order, OrderItem
from .serializers import (
    FarmerOrderSerializer,
    FarmerOrderStatusSerializer,
    OrderPlacementSerializer,
)


User = get_user_model()


class OrderPlacementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != "BUYER":
            return Response(
                {"detail": "Only buyers can place orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = OrderPlacementSerializer(data=request.data)

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        product_id = serializer.validated_data["product_id"]
        quantity = serializer.validated_data["quantity"]

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if quantity > product.quantity_available:
            return Response(
                {
                    "detail": (
                        f"Only {product.quantity_available} units "
                        "are available."
                    )
                },
                status=status.HTTP_400_BAD_REQUEST,
            )

        total_amount = product.price_per_unit * quantity

        with transaction.atomic():
            order = Order.objects.create(
                buyer=request.user,
                status="placed",
                total_amount=total_amount,
            )

            OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_order=product.price_per_unit,
            )

            product.quantity_available -= quantity
            product.save(update_fields=["quantity_available"])

        return Response(
            {
                "message": "Order placed successfully.",
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
                "product": product.name,
                "quantity": quantity,
                "price_at_order": product.price_per_unit,
            },
            status=status.HTTP_201_CREATED,
        )


class FarmerOrderPagination(PageNumberPagination):
    page_size = 10


class FarmerOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.FARMER:
            return Response(
                {"detail": "Only farmers can view farmer orders."},
                status=status.HTTP_403_FORBIDDEN,
            )

        farmer_items = (
            OrderItem.objects
            .filter(product__farmer=request.user)
            .select_related("product")
        )

        orders = (
            Order.objects
            .filter(items__product__farmer=request.user)
            .select_related("buyer")
            .prefetch_related(
                Prefetch(
                    "items",
                    queryset=farmer_items,
                    to_attr="farmer_items",
                )
            )
            .distinct()
            .order_by("-created_at")
        )

        paginator = FarmerOrderPagination()
        page = paginator.paginate_queryset(orders, request)

        serializer = FarmerOrderSerializer(
            page,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(serializer.data)


class FarmerOrderStatusUpdateView(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, order_id):
        if request.user.role != User.FARMER:
            return Response(
                {"detail": "Only farmers can update order status."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = (
                Order.objects
                .filter(
                    id=order_id,
                    items__product__farmer=request.user,
                )
                .distinct()
                .get()
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = FarmerOrderStatusSerializer(
            order,
            data=request.data,
            partial=True,
        )

        if not serializer.is_valid():
            return Response(
                serializer.errors,
                status=status.HTTP_400_BAD_REQUEST,
            )

        serializer.save()

        return Response(
            {
                "message": "Order status updated successfully.",
                "order_id": order.id,
                "status": order.status,
            },
            status=status.HTTP_200_OK,
        )