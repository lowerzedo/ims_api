"""Admin configuration for the custom user model."""
from __future__ import annotations

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserChangeForm, UserCreationForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    ordering = ("email",)
    add_form = UserCreationForm
    form = UserChangeForm
    model = User
    list_display = (
        "email",
        "first_name",
        "last_name",
        "role",
        "can_produce",
        "can_manage_accounts",
        "is_active",
        "is_staff",
    )
    list_filter = ("role", "can_produce", "can_manage_accounts", "is_active", "is_staff")
    search_fields = ("email", "first_name", "last_name")
    readonly_fields = ("last_login", "date_joined", "created_at", "updated_at")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Personal info", {"fields": ("first_name", "last_name", "phone_number")}),
        (
            "Capabilities",
            {
                "fields": ("can_produce", "can_manage_accounts"),
                "description": "What roles this user can perform on policies.",
            },
        ),
        (
            "Default Commission Rates",
            {
                "fields": ("default_producer_rate", "default_account_manager_rate"),
                "description": "Default rates applied when user is assigned to policies. Can be overridden per policy.",
            },
        ),
        (
            "Permissions",
            {
                "fields": ("role", "is_active", "is_staff", "is_superuser", "groups", "user_permissions"),
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined", "created_at", "updated_at")}),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "password1",
                    "password2",
                    "can_produce",
                    "can_manage_accounts",
                    "is_staff",
                    "is_superuser",
                ),
            },
        ),
    )
