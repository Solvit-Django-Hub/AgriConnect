from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from .models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display = (
        "username",
        "email",
        "phone_number",
        "role",
        "is_staff",
        "is_active",
    )

    list_filter = (
        "role",
        "is_staff",
        "is_active",
    )

    search_fields = (
        "username",
        "email",
        "phone_number",
    )

    fieldsets = UserAdmin.fieldsets + (
        (
            "AgriConnect Information",
            {
                "fields": (
                    "role",
                    "phone_number",
                )
            },
        ),
    )

    add_fieldsets = UserAdmin.add_fieldsets + (
        (
            "AgriConnect Information",
            {
                "fields": (
                    "role",
                    "phone_number",
                )
            },
        ),
    )
