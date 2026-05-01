from rest_framework import serializers
from .models import Order, OrderItem, BankPaymentDetails, CashPickupDetails


class OrderItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(source="product.name", read_only=True)
    deal_name = serializers.CharField(source="deal.title", read_only=True)
    subtotal = serializers.SerializerMethodField()

    class Meta:
        model = OrderItem
        fields = [
            "id",
            "product",
            "product_name",
            "deal",
            "deal_name",
            "quantity",
            "price_at_purchase",
            "subtotal",
        ]

    def get_subtotal(self, obj):
        return obj.subtotal()


class BankPaymentDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = BankPaymentDetails
        fields = ["phone_used", "note"]


class CashPickupDetailsSerializer(serializers.ModelSerializer):
    class Meta:
        model = CashPickupDetails
        fields = ["pickup_name", "pickup_phone"]


class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    bank_details = BankPaymentDetailsSerializer(read_only=True)
    cash_details = CashPickupDetailsSerializer(read_only=True)

    class Meta:
        model = Order
        fields = [
            "id",
            "email",
            "payment_method",
            "total_price",
            "status",
            "created_at",
            "latitude",
            "longitude",
            "distance_from_kafei",
            "items",
            "bank_details",
            "cash_details",
        ]
        read_only_fields = ["id", "total_price", "status", "created_at"]
