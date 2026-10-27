from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import NotificationPreference


@admin.register(NotificationPreference)
class NotificationPreferenceAdmin(admin.ModelAdmin):
    list_display = (
        "user",
        "order_updates",
        "offers_deals",
        "wishlist_alerts",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
        "updated_at",
    )

    list_filter = (
        "order_updates",
        "offers_deals",
        "email_notifications",
        "sms_notifications",
        "push_notifications",
    )

    search_fields = ("user__username", "user__email")
    readonly_fields = ("updated_at",)