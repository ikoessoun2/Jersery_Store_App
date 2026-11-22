# from .models import Inventory


# class InventoryRepository:

#     @staticmethod
#     def get_by_variant(variant_id: int):
#         return (
#             Inventory.objects
#             .select_related("variant")
#             .filter(variant_id=variant_id)
#             .first()
#         )

#     @staticmethod
#     def get_by_id(inventory_id: int):
#         return (
#             Inventory.objects
#             .select_related("variant")
#             .filter(id=inventory_id)
#             .first()
#         )

#     @staticmethod
#     def get_all():
#         return (
#             Inventory.objects
#             .select_related("variant")
#             .all()
#         )

#     @staticmethod
#     def create(variant_id: int, quantity: int = 0):
#         return Inventory.objects.create(
#             variant_id=variant_id,
#             quantity=quantity
#         )