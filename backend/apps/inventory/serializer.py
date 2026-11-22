
# from rest_framework import serializers

# from apps.inventory.models import Inventory


# class InventorySerializer(serializers.ModelSerializer):

#     variant_sku = serializers.CharField(
#         source="variant.sku",
#         read_only=True
#     )

#     class Meta:
#         model = Inventory
#         fields = [
#             "id",
#             "variant",
#             "variant_sku",
#             "quantity",
#             "created_at",
#             "updated_at",
#         ]
#         read_only_fields = [
#             "id",
#             "variant_sku",
#             "created_at",
#             "updated_at",
#         ]
