from django.db import transaction
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from farmers.models import Product

from .models import Order, OrderItem
from .serializers import OrderPlacementSerializer


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