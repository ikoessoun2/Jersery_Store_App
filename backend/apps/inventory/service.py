
# from django.db import transaction
# from django.core.exceptions import ValidationError

# from .repository import InventoryRepository


# class InventoryService:

#     @staticmethod
#     def get_by_variant(variant_id: int):
#         inventory = InventoryRepository.get_by_variant(variant_id)

#         if inventory is None:
#             raise ValidationError("Inventory record not found for this variant.")

#         return inventory

#     @staticmethod
#     def get_by_id(inventory_id: int):
#         inventory = InventoryRepository.get_by_id(inventory_id)

#         if inventory is None:
#             raise ValidationError("Inventory record not found.")

#         return inventory

#     @staticmethod
#     def get_all():
#         return InventoryRepository.get_all()

#     @staticmethod
#     @transaction.atomic
#     def create(variant_id: int, quantity: int = 0):
#         if quantity < 0:
#             raise ValidationError("Inventory quantity cannot be negative.")

#         existing_inventory = InventoryRepository.get_by_variant(variant_id)

#         if existing_inventory:
#             raise ValidationError("Inventory already exists for this variant.")

#         return InventoryRepository.create(
#             variant_id=variant_id,
#             quantity=quantity
#         )
