from django.contrib import admin

from .models import Category, Order, OrderItem


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = (
        "name",
    )

    search_fields = (
        "name",
    )


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = (
        "price_at_order",
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "buyer",
        "status",
        "total_amount",
        "created_at",
    )

    list_filter = (
        "status",
        "created_at",
    )

    search_fields = (
        "buyer__username",
        "buyer__phone_number",
    )

    readonly_fields = (
        "total_amount",
        "created_at",
    )

    inlines = (
        OrderItemInline,
    )


@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = (
        "order",
        "product",
        "quantity",
        "price_at_order",
    )

    search_fields = (
        "product__name",
        "order__buyer__username",
    )

    readonly_fields = (
        "price_at_order",
    )
