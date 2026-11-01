from .repository import CategoryRepository
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

        CategoryRepository.delete(category_id)