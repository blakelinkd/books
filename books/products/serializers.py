from rest_framework import serializers
from .models import Product

class ProductSerializer(serializers.ModelSerializer):
    price = serializers.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        model = Product
        fields = ['id', 'name', 'description', 'price', 'inventory', 'created_at', 'updated_at']

    def validate(self, data):
        if data['price'] <= 0:
            raise serializers.ValidationError("Price must be greater than 0.")
        if data['inventory'] < 0:
            raise serializers.ValidationError("Inventory must be greater than or equal to 0.")
        return data

    def create(self, validated_data):
        return super().create(validated_data)