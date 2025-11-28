from django.contrib import admin
from .models import Order, OrderItem, BankPaymentDetails, CashPickupDetails

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0

class BankDetailsInline(admin.StackedInline):
    model = BankPaymentDetails
    extra = 0

class CashDetailsInline(admin.StackedInline):
    model = CashPickupDetails
    extra = 0

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "payment_method", "total_price", "status", "created_at")
    list_filter = ("payment_method", "status")
    inlines = [OrderItemInline, BankDetailsInline, CashDetailsInline]

admin.site.register(OrderItem)
