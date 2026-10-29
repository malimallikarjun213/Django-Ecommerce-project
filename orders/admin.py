from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Order, OrderItem


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "full_name",
        "phone",
        "final_amount",
        "payment_method",
        "payment_status",
        "status",
        "created_at",
    )

    list_filter = ("status", "payment_status", "payment_method")
    search_fields = ("full_name", "email", "phone")
    inlines = [OrderItemInline]


admin.site.register(OrderItem)