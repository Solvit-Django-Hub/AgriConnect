from django.contrib import admin

from .models import Buyer


@admin.register(Buyer)
class BuyerAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "gender",
    )

    list_filter = (
        "gender",
    )

    search_fields = (
        "user__username",
        "user__email",
        "user__phone_number",
    )
