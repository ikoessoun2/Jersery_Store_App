from unicodedata import category

from .repository import CategoryRepository, ProductRepository
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



