from django.contrib.auth import get_user_model
from django.db import transaction
from django.db.models import F, Sum
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from farmers.models import Product

from .models import Order, OrderItem
from .serializers import OrderPlacementSerializer


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