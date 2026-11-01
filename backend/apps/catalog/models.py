from django.db import models

# Create your models here.

class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField(blank=True)
    deleted = models.BooleanField(default=False)

    def __str__(self):
        return self.name
    
class Product(models.Model):
    category = models.ForeignKey(
        "catalog.Category",
        on_delete=models.PROTECT,
        related_name="products"
    )
    name = models.CharField(max_length=200)
    description = models.TextField()

    deleted = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name   






# class Size(models.Model):
#     name = models.CharField(max_length=20, unique=True)

#     def __str__(self):
#         return self.name


# class ProductVariant(models.Model):
#     product = models.ForeignKey(
#         "catalog.Product",
#         on_delete=models.CASCADE,
#         related_name="variants"
#     )
#     size = models.ForeignKey(
#         "catalog.Size",
#         on_delete=models.PROTECT,
#         related_name="product_variants"
#     )
#     sku = models.CharField(max_length=100, unique=True)
#     price = models.DecimalField(max_digits=10, decimal_places=2)

#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["product", "size"],
#                 name="unique_product_size"
#             )
#         ]

#     def __str__(self):
#         return f"{self.product.name} - {self.size.name}"


# class ProductImage(models.Model):
#     product = models.ForeignKey(
#         "catalog.Product",
#         on_delete=models.CASCADE,
#         related_name="images"
#     )
#     image = models.ImageField(upload_to="products/")
#     is_primary = models.BooleanField(default=False)
#     alt_text = models.CharField(max_length=255, blank=True)
    
#     class Meta:
#         constraints = [
#             models.UniqueConstraint(
#                 fields=["product"],
#                 condition=models.Q(is_primary=True),
#                 name="unique_primary_image_per_product"
#             )
#         ]

#     def __str__(self):
#         return f"{self.product.name} - Image"




