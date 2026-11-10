from django.db import IntegrityError, transaction
from rest_framework.exceptions import ValidationError

from django.db import IntegrityError, transaction
from .repository import CategoryRepository, ProductRepository, SizeRepository, ProductVariantRepository, ProductImageRepository
from .exceptions import ResourceNotFoundException, ResourceConflictException

class CategoryService:

    @staticmethod
    def get_all_categories():
        return CategoryRepository.get_all()

    @staticmethod
    def get_category_by_id(category_id):
        category = CategoryRepository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundException(
                detail=f"Category with ID {category_id} not found."
            )

        return category

    @staticmethod
    def create_category(name, description):
        category = CategoryRepository.get_by_name(name)

        if category is not None:
            raise ResourceConflictException(
                detail=f"Category with name '{name}' already exists."
            )

        category = CategoryRepository.create(name, description)
        return category

    @staticmethod
    def update_category(category_id, name, description):
        category = CategoryRepository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundException(
                detail=f"Category with ID {category_id} not found."
            )

        category.name = name
        category.description = description
        category.save()
        return category

    @staticmethod
    def delete_category(category_id):
        category = CategoryRepository.get_by_id(category_id)

        if category is None:
            raise ResourceNotFoundException(
                detail=f"Category with ID {category_id} not found."
            )
        if category.products.exists():
            raise ResourceConflictException(
                detail="Cannot delete a category that has associated products."
        )

        CategoryRepository.delete(category_id)



class ProductService:

    @staticmethod
    def get_all_products():
        products = ProductRepository.get_all()
        if not products:
            raise ResourceNotFoundException(detail="No products found.")
        return products

    @staticmethod
    def get_product_by_id(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ResourceNotFoundException(
                detail=f"Product with ID {product_id} not found."
            )
        return product

    @staticmethod
    def create_product(category_id, name, description):
        category = CategoryRepository.get_by_id(category_id)

        if not category:
            raise ResourceNotFoundException(
                detail=f"Category with ID {category_id} not found."
            )

        product = ProductRepository.create(category, name, description)
        return product


    @staticmethod
    def update_product(product_id, category=None, name=None, description=None):

        product = ProductRepository.get_by_id(product_id)

        if not product or product.deleted:
            raise ResourceNotFoundException(
                detail=f"Product with ID {product_id} not found."
            )

        if category is not None and category.deleted:
            raise ResourceNotFoundException(
                detail="Category was not found."
            )

        if name is not None:
            existing_product = ProductRepository.get_by_name(name)

            if existing_product and existing_product.id != product.id:
                raise ResourceConflictException(
                    detail=f"Product with name '{name}' already exists."
                )

        return ProductRepository.update(
            product=product,
            category=category,
            name=name,
            description=description
        )

    def delete_product(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ResourceNotFoundException(
                detail=f"Product with ID {product_id} not found."
            )

        ProductRepository.delete(product)


class SizeService:

    @staticmethod
    def get_all_sizes():
        return SizeRepository.get_all()

    @staticmethod
    def get_size_by_id(size_id):
        size = SizeRepository.get_by_id(size_id)

        if not size:
            raise ResourceNotFoundException(
                detail=f"Size with ID {size_id} not found."
            )
        return size

    @staticmethod
    def get_size_by_name(name):
        size = SizeRepository.get_by_name(name)

        if not size:
            raise ResourceNotFoundException(
                detail=f"Size with name '{name}' not found."
            )
        return size

    @staticmethod
    def create_size(name):
        existing_size = SizeRepository.get_by_name(name)

        if existing_size:
            raise ResourceConflictException(
                detail=f"Size with name '{name}' already exists."
            )

        return SizeRepository.create(name)

    @staticmethod
    def update_size(size_id, name):
        size = SizeRepository.get_by_id(size_id)

        if not size:
            raise ResourceNotFoundException(
                detail=f"Size with ID {size_id} not found."
            )

        existing_size = SizeRepository.get_by_name(name)

        if existing_size and existing_size.id != size.id:
            raise ResourceConflictException(
                detail=f"Size with name '{name}' already exists."
            )

        size.name = name
        size.save()
        return size



class ProductVariantService:

    @staticmethod
    def create_product_variant(product_id, size_id, sku, price):
        product = ProductRepository.get_by_id(product_id)
        if not product:
            raise ValueError("Product does not exist.")

        size = SizeRepository.get_by_id(size_id)
        if not size:
            raise ValueError("Size does not exist.")

        try:
            with transaction.atomic():
                return ProductVariantRepository.create(
                    product=product,
                    size=size,
                    sku=sku,
                    price=price
                )
        except IntegrityError:
            raise ValueError(
                "A product variant with this SKU or product-size combination already exists."
            )

    @staticmethod
    def get_product_variant_by_id(variant_id):
        variant = ProductVariantRepository.get_by_id(variant_id)

        if not variant:
            raise ValueError("Product variant not found.")

        return variant

    @staticmethod
    def get_all_product_variants():
        return ProductVariantRepository.get_all()

    @staticmethod
    def get_product_variants_by_product(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ValueError("Product does not exist.")

        return ProductVariantRepository.get_by_product(product_id)

    @staticmethod
    def get_product_variants_by_size(size_id):
        size = SizeRepository.get_by_id(size_id)

        if not size:
            raise ValueError("Size does not exist.")

        return ProductVariantRepository.get_by_size(size_id)

    @staticmethod
    def get_product_variant_by_sku(sku):
        variant = ProductVariantRepository.get_by_sku(sku)

        if not variant:
            raise ValueError("Product variant not found.")

        return variant

    @staticmethod
    def update_product_variant(variant_id, **kwargs):
        variant = ProductVariantService.get_product_variant_by_id(
            variant_id
        )

        if "product_id" in kwargs:
            product = ProductRepository.get_by_id(kwargs["product_id"])

            if not product:
                raise ValueError("Product does not exist.")

            kwargs["product"] = product
            del kwargs["product_id"]

        if "size_id" in kwargs:
            size = SizeRepository.get_by_id(kwargs["size_id"])

            if not size:
                raise ValueError("Size does not exist.")

            kwargs["size"] = size
            del kwargs["size_id"]

        allowed_fields = {"product", "size", "sku", "price"}

        invalid_fields = set(kwargs.keys()) - allowed_fields

        if invalid_fields:
            raise ValueError(
                f"Invalid fields: {', '.join(invalid_fields)}"
            )

        try:
            with transaction.atomic():
                return ProductVariantRepository.update(
                    variant.id,
                    **kwargs
                )
        except IntegrityError:
            raise ValueError(
                "A product variant with this SKU or product-size combination already exists."
            )

    @staticmethod
    def delete_product_variant(variant_id):
        ProductVariantService.get_product_variant_by_id(variant_id)

        return ProductVariantRepository.delete(variant_id)


class ProductImageService:

    @staticmethod
    def get_all_images():
        return ProductImageRepository.get_all()

    @staticmethod
    def get_image_by_id(image_id):
        image = ProductImageRepository.get_by_id(image_id)

        if not image:
            raise ValidationError("Product image not found.")

        return image

    @staticmethod
    def get_images_by_product(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ValidationError("Product not found.")

        return ProductImageRepository.get_by_product(product_id)

    @staticmethod
    def get_primary_image(product_id):
        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ValidationError("Product not found.")

        return ProductImageRepository.get_primary_image(product_id)

    @staticmethod
    @transaction.atomic
    def create_image(data):
        product_id = data.get("product")

        product = ProductRepository.get_by_id(product_id)

        if not product:
            raise ValidationError("Product not found.")

        is_primary = data.get("is_primary", False)

        if is_primary:
            ProductImageRepository.get_by_product(product_id).filter(
                is_primary=True
            ).update(is_primary=False)

        try:
            return ProductImageRepository.create(data)

        except IntegrityError:
            raise ValidationError(
                "A primary image already exists for this product."
            )

    @staticmethod
    @transaction.atomic
    def update_image(image_id, data):
        image = ProductImageService.get_image_by_id(image_id)

        product_id = image.product_id

        is_primary = data.get("is_primary", image.is_primary)

        if is_primary:
            ProductImageRepository.get_by_product(product_id).exclude(
                id=image.id
            ).filter(is_primary=True).update(is_primary=False)

        try:
            return ProductImageRepository.update(image, data)

        except IntegrityError:
            raise ValidationError(
                "A primary image already exists for this product."
            )

    @staticmethod
    def delete_image(image_id):
        image = ProductImageService.get_image_by_id(image_id)

        ProductImageRepository.delete(image)

        return True