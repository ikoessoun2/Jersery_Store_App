
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.test import APITestCase

# from apps.inventory.models import Inventory
# from apps.catalog.models import Product, ProductVariant, Size


# class InventoryAPITests(APITestCase):

#     def setUp(self):
#         self.product = Product.objects.create(
#             # Add your required Product fields
#         )

#         self.size = Size.objects.create(
#             # Add your required Size fields
#         )

#         self.variant = ProductVariant.objects.create(
#             # Add your required ProductVariant fields
#         )

#         self.inventory = Inventory.objects.create(
#             variant=self.variant,
#             quantity=10
#         )

#         self.list_url = "/api/inventory/"

#     def test_list_inventory(self):
#         response = self.client.get(self.list_url)

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(len(response.data), 1)

#     def test_retrieve_inventory(self):
#         response = self.client.get(
#             f"{self.list_url}{self.inventory.id}/"
#         )

#         self.assertEqual(response.status_code, status.HTTP_200_OK)
#         self.assertEqual(response.data["quantity"], 10)

#     def test_retrieve_nonexistent_inventory(self):
#         response = self.client.get(
#             f"{self.list_url}99999/"
#         )

#         self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

#     def test_create_inventory(self):
#         # Create a second variant using your model's required fields.
#         # Then submit its ID to the endpoint.

#         pass

#     def test_create_inventory_with_negative_quantity(self):
#         response = self.client.post(
#             self.list_url,
#             {
#                 "variant": self.variant.id,
#                 "quantity": -5
#             },
#             format="json"
#         )

#         self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
