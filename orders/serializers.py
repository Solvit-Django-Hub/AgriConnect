from rest_framework import serializers

from .models import Order, OrderItem


class OrderPlacementSerializer(serializers.Serializer):
    product_id = serializers.IntegerField()
    quantity = serializers.IntegerField(min_value=1)


class FarmerOrderItemSerializer(serializers.ModelSerializer):
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


class FarmerOrderSerializer(serializers.ModelSerializer):
    items = FarmerOrderItemSerializer(
        source="farmer_items",
        many=True,
        read_only=True,
    )

    buyer = serializers.CharField(
        source="buyer.username",
        read_only=True,
    )

    class Meta:
        model = Order
        fields = [
            "id",
            "buyer",
            "status",
            "total_amount",
            "created_at",
            "items",
        ]


class FarmerOrderStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = ["status"]