from rest_framework import serializers

from farmers.models import Product


class BuyerProductSerializer(serializers.ModelSerializer):
    farmer = serializers.CharField(source="farmer.username", read_only=True)

    class Meta:
        model = Product
        fields = [
            "id",
            "name",
            "price_per_unit",
            "quantity_available",
            "category",
            "farmer",
            "created_at",
        ]
        read_only_fields = fields