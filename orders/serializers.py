from rest_framework import serializers

from .models import Order, OrderItem


class OrderPlacementSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class BuyerOrderItemSerializer(serializers.ModelSerializer):
    product = serializers.CharField(
        source="product.name",
        read_only=True,
    )

    class Meta:
        model = OrderItem
        fields = [
            "product",
            "quantity",
            "price_at_order",
        ]


class BuyerOrderSerializer(serializers.ModelSerializer):
    items = BuyerOrderItemSerializer(
        many=True,
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]