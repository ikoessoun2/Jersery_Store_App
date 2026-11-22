from rest_framework import serializers
from .models import Category, Product, Size, ProductVariant, ProductImage

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name', 'description']

class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = ['id', 'category', 'name', 'description']

class SizeSerializer(serializers.ModelSerializer):

    class Meta:
        model = Size
        fields = ['id', 'name']
        read_only_fields = ['id']

    def validate_name(self, value):
        if not value.strip():
            raise serializers.ValidationError(
                "Size name cannot be empty."
            )

        return value.strip()

class ProductVariantSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProductVariant
        fields = [
            "id",
            "product",
            "size",
            "sku",
            "price",
        ]
        read_only_fields = ["id"]

    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "is_primary",
            "alt_text",
        ]
        read_only_fields = ["id"]

class ProductImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = ProductImage
        fields = [
            "id",
            "product",
            "image",
            "is_primary",
            "alt_text",
        ]
        read_only_fields = ["id"]