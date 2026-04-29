from rest_framework import serializers
from .models import MenuItem, Category


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = '__all__'


class MenuItemSerializer(serializers.ModelSerializer):
    category = CategorySerializer()  # shows full category details

    class Meta:
        model = MenuItem
        fields = '__all__'