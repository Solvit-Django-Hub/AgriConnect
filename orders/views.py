from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F, Prefetch, Sum
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from farmers.models import Product

from .models import Order, OrderItem
from .serializers import (
    BuyerOrderSerializer,
    FarmerOrderSerializer,
    FarmerOrderStatusSerializer,
    OrderPlacementSerializer,
)


User = get_user_model()


class OrderPlacementView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        if request.user.role != User.BUYER:
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

        with transaction.atomic():
            order = Order.objects.create(
                buyer=request.user,
                status="placed",
            )

            order_item = OrderItem.objects.create(
                order=order,
                product=product,
                quantity=quantity,
                price_at_order=product.price_per_unit,
            )

            total_amount = order.items.aggregate(
                total=Sum(
                    F("quantity") * F("price_at_order")
                )
            )["total"]

            order.total_amount = total_amount
            order.save(update_fields=["total_amount"])

            product.quantity_available -= quantity
            product.save(update_fields=["quantity_available"])

        return Response(
            {
                "message": "Order placed successfully.",
                "order_id": order.id,
                "status": order.status,
                "total_amount": order.total_amount,
                "product": product.name,
                "quantity": order_item.quantity,
                "price_at_order": order_item.price_at_order,
            },
            status=status.HTTP_201_CREATED,
        )


class BuyerOrderPagination(PageNumberPagination):
    page_size = 10


class BuyerOrderListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != User.BUYER:
            return Response(
                {"detail": "Only buyers can view order history."},
                status=status.HTTP_403_FORBIDDEN,
            )

        orders = (
            Order.objects
            .filter(buyer=request.user)
            .prefetch_related("items__product")
            .order_by("-created_at")
        )

        paginator = BuyerOrderPagination()
        page = paginator.paginate_queryset(orders, request)

        serializer = BuyerOrderSerializer(
            page,
            many=True,
            context={"request": request},
        )

        return paginator.get_paginated_response(serializer.data)


class BuyerOrderDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, order_id):
        if request.user.role != User.BUYER:
            return Response(
                {"detail": "Only buyers can view order details."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            order = (
                Order.objects
                .filter(
                    id=order_id,
                    buyer=request.user,
                )
                .prefetch_related("items__product")
                .get()
            )
        except Order.DoesNotExist:
            return Response(
                {"detail": "Order not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BuyerOrderSerializer(
            order,
            context={"request": request},
        )

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
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
