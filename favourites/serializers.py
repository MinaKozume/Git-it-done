from rest_framework import serializers
from .models import FavouriteItem

class FavouriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = FavouriteItem
        fields = '__all__'