from .models import Category, Product


class CategoryRepository:

    @staticmethod
    def get_all():
        categories =Category.objects.all()
        categories = categories.filter(deleted=False)
        return categories

    @staticmethod
    def get_by_id(category_id):
        return Category.objects.filter(id=category_id, deleted=False).first()

    @staticmethod
    def get_by_name(name):
        return Category.objects.filter(name__iexact=name, deleted=False).first()

    @staticmethod
    def create(name, description=""):
        return Category.objects.create(
            name=name,
            description=description
        )

    @staticmethod
    def update(category_id, **kwargs):
        category = CategoryRepository.get_by_id(category_id)

        if category is None:
            return None
        if category.deleted:
            return None

        for field, value in kwargs.items():
            if field in {"name", "description"}:
                setattr(category, field, value)

        category.save()
        return category

    @staticmethod
    def delete(category_id):
        category = CategoryRepository.get_by_id(category_id)

        if category is None:
            return False

        category.deleted = True
        category.save()
        return True


class ProductRepository:

    @staticmethod
    def get_all():
        products = Product.objects.select_related('category').all()
        products = products.filter(deleted=False)
        return products

    @staticmethod
    def get_by_id(product_id):
        product = Product.objects.filter(id=product_id, deleted=False).first()
        if not product:
            return None
        else:
            return product

    @staticmethod
    def get_by_name(name):
        product = Product.objects.filter(name=name, deleted=False).first()
        if not product:
            return None
        else:
            return product 

    @staticmethod
    def create(category, name, description):
        return Product.objects.create(
            category=category,
            name=name,
            description=description
        )


    @staticmethod
    def update(product, category=None, name=None, description=None):

        if product is None or product.deleted:
            return None

        if category is not None:
            product.category = category

        if name is not None:
            product.name = name

        if description is not None:
            product.description = description

        product.save()

        return product

    @staticmethod
    def delete(product):
        product.deleted = True
        product.save()





















# class ProductRepository:

#     @staticmethod
#     def get_all():
#         return Product.objects.select_related("category").all()

#     @staticmethod
#     def get_by_id(product_id):
#         return Product.objects.select_related("category").filter(
#             id=product_id
#         ).first()

#     @staticmethod
#     def get_by_name(name):
#         return Product.objects.filter(name__iexact=name).first()

#     @staticmethod
#     def get_by_category(category_id):
#         return Product.objects.filter(
#             category_id=category_id
#         ).select_related("category")

#     @staticmethod
#     def create(category, name, description):
#         return Product.objects.create(
#             category=category,
#             name=name,
#             description=description
#         )

#     @staticmethod
#     def update(product_id, **kwargs):
#         product = ProductRepository.get_by_id(product_id)

#         if product is None:
#             return None

#         allowed_fields = {"category", "name", "description"}

#         for field, value in kwargs.items():
#             if field in allowed_fields:
#                 setattr(product, field, value)

#         product.save()
#         return product

#     @staticmethod
#     def delete(product_id):
#         product = ProductRepository.get_by_id(product_id)

#         if product is None:
#             return False

#         product.delete()
#         return True


# class SizeRepository:

#     @staticmethod
#     def get_all():
#         return Size.objects.all()

#     @staticmethod
#     def get_by_id(size_id):
#         return Size.objects.filter(id=size_id).first()

#     @staticmethod
#     def get_by_name(name):
#         return Size.objects.filter(name__iexact=name).first()

#     @staticmethod
#     def create(name):
#         return Size.objects.create(name=name)

#     @staticmethod
#     def update(size_id, **kwargs):
#         size = SizeRepository.get_by_id(size_id)

#         if size is None:
#             return None

#         if "name" in kwargs:
#             size.name = kwargs["name"]

#         size.save()
#         return size

#     @staticmethod
#     def delete(size_id):
#         size = SizeRepository.get_by_id(size_id)

#         if size is None:
#             return False

#         size.delete()
#         return True


# class ProductVariantRepository:

#     @staticmethod
#     def get_all():
#         return ProductVariant.objects.select_related(
#             "product", "size"
#         ).all()

#     @staticmethod
#     def get_by_id(variant_id):
#         return ProductVariant.objects.select_related(
#             "product", "size"
#         ).filter(id=variant_id).first()

#     @staticmethod
#     def get_by_sku(sku):
#         return ProductVariant.objects.filter(sku__iexact=sku).first()

#     @staticmethod
#     def get_by_product(product_id):
#         return ProductVariant.objects.filter(
#             product_id=product_id
#         ).select_related("product", "size")

#     @staticmethod
#     def get_by_size(size_id):
#         return ProductVariant.objects.filter(
#             size_id=size_id
#         ).select_related("product", "size")

#     @staticmethod
#     def create(product, size, sku, price):
#         return ProductVariant.objects.create(
#             product=product,
#             size=size,
#             sku=sku,
#             price=price
#         )

#     @staticmethod
#     def update(variant_id, **kwargs):
#         variant = ProductVariantRepository.get_by_id(variant_id)

#         if variant is None:
#             return None

#         allowed_fields = {"product", "size", "sku", "price"}

#         for field, value in kwargs.items():
#             if field in allowed_fields:
#                 setattr(variant, field, value)

#         variant.save()
#         return variant

#     @staticmethod
#     def delete(variant_id):
#         variant = ProductVariantRepository.get_by_id(variant_id)

#         if variant is None:
#             return False

#         variant.delete()
#         return True


# class ProductImageRepository:

#     @staticmethod
#     def get_all():
#         return ProductImage.objects.select_related("product").all()

#     @staticmethod
#     def get_by_id(image_id):
#         return ProductImage.objects.select_related(
#             "product"
#         ).filter(id=image_id).first()

#     @staticmethod
#     def get_by_product(product_id):
#         return ProductImage.objects.filter(
#             product_id=product_id
#         ).select_related("product")

#     @staticmethod
#     def get_primary_image(product_id):
#         return ProductImage.objects.filter(
#             product_id=product_id,
#             is_primary=True
#         ).first()

#     @staticmethod
#     def create(product, image, alt_text="",
#                is_primary=False):
#         return ProductImage.objects.create(
#             product=product,
#             image=image,
#             alt_text=alt_text,
#             is_primary=is_primary
#         )

#     @staticmethod
#     def update(image_id, **kwargs):
#         product_image = ProductImageRepository.get_by_id(image_id)

#         if product_image is None:
#             return None

#         allowed_fields = {
#             "product",
#             "image",
#             "alt_text",
#             "is_primary"
#         }

#         for field, value in kwargs.items():
#             if field in allowed_fields:
#                 setattr(product_image, field, value)

#         product_image.save()
#         return product_image

#     @staticmethod
#     def delete(image_id):
#         product_image = ProductImageRepository.get_by_id(image_id)

#         if product_image is None:
#             return False

#         product_image.delete()
#         return True









