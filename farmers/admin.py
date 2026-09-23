from django.contrib import admin

from .models import Farmer, Product


@admin.register(Farmer)
class FarmerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__phone_number",
    )


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "farmer",
        "category",
        "price_per_unit",
        "quantity_available",
        "created_at",
    )

    list_filter = (
        "category",
        "created_at",
    )

    search_fields = (
        "name",
        "farmer__username",
        "farmer__phone_number",
    )

    readonly_fields = (
        "created_at",
    )
