from rest_framework.test import APITestCase
from django.urls import reverse
from rest_framework import status
from .models import Category, Product, Size

class CategoryManagementTests(APITestCase):
    def setUp(self):
        self.list_url = reverse('category-list')

        self.category = Category.objects.create(
            name="Test Category", 
            description="A test category."
        )

        self.detail_url = reverse(
            'category-detail',
            kwargs={'pk': self.category.id}
        )

    def test_list_categories(self):
        # Arrange
        Category.objects.create(
            name="Another Category",
            description="Another test category."
        )

        # Act
        response = self.client.get(self.list_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)

    # RETRIEVE CATEGORY
    def test_retrieve_category(self):

        # Arrange
        expected_name = self.category.name

        # Act
        response  = self.client.get(self.detail_url)
    
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], expected_name)

    def test_retrieve_nonexistent_category(self):
        # Arrange
        non_existent_id = 999
        url = reverse(
            'category-detail',
            kwargs={'pk': non_existent_id}
            )

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # CREATE CATEGORY
    def test_create_category(self):
        # Arrange
        data = {
            "name": "Furniture",
            "description": "Furniture products."
        }

        # Act
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertTrue(Category.objects.filter(name=data['name']).exists())

    def test_create_category_with_existing_name(self):
        # Arrange
        data = {
            "name": self.category.name,  # Using the name of the existing category
            "description": "Duplicate category."
        }

        # Act
        response = self.client.post(
            self.list_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_409_CONFLICT)

    # UPDATE CATEGORY
    def test_update_category(self):
        # Arrange
        data = {
            "name": "Updated Category",
            "description": "Updated description."
        }

        # Act
        response = self.client.put(
            self.detail_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.category.refresh_from_db()

        self.assertEqual(self.category.name, data['name'])
        self.assertEqual(self.category.description, data['description'])

    def test_update_nonexistent_category(self):
        # Arrange
        non_existent_id = 999
        url = reverse(
            'category-detail',
            kwargs={'pk': non_existent_id}
        )
        data = {
            "name": "Nonexistent Category",
            "description": "This category does not exist."
        }

        # Act
        response = self.client.put(
            url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    # DELETE CATEGORY
    def test_delete_category(self):
        # Act
        response = self.client.delete(self.detail_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Category.objects.filter(id=self.category.id).exists())
        self.category.refresh_from_db()
        self.assertTrue(self.category.deleted)

class ProductManagementTests(APITestCase):
    def setUp(self):
        self.category = Category.objects.create(
            name="Test Category", 
            description="A test category."
        )
        self.category_url = reverse('category-detail', kwargs={'pk': self.category.id})

        self.product = Product.objects.create(
            category=self.category,
            name="Test Product",
            description="A test product."
        )
        self.product_list_url = reverse('product-list')
        self.product_detail_url = reverse('product-detail', kwargs={'pk': self.product.id})


    def test_list_products(self):
        # Arrange
        Product.objects.create(
            category=self.category,
            name="Another Product",
            description="Another test product."
        )

        # Act
        response = self.client.get(self.product_list_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 2)


    def test_retrieve_product(self):
        # Arrange
        expected_name = self.product.name

        # Act
        response  = self.client.get(self.product_detail_url)
    
        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], expected_name)

    def test_retrieve_nonexistent_product(self):
        # Arrange
        non_existent_id = 999
        url = reverse(
            'product-detail',
            kwargs={'pk': non_existent_id}
            )

        # Act
        response = self.client.get(url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_product(self):
        # Arrange
        data = {
            "category": self.category.id,
            "name": "New Product",
            "description": "A new test product."
        }

        # Act
        response = self.client.post(
            self.product_list_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], data['name'])
        self.assertTrue(Product.objects.filter(name=data['name']).exists())

    def test_create_product_with_nonexistent_category(self):
        # Arrange
        non_existent_category_id = 999
        data = {
            "category": non_existent_category_id,
            "name": "Product with Nonexistent Category",
            "description": "This product has a category that does not exist."
        }

        # Act
        response = self.client.post(
            self.product_list_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_update_product(self):
        # Arrange
        data = {
            "name": "Updated Product",
            "description": "Updated product description."
        }

        # Act
        response = self.client.patch(
            self.product_detail_url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        self.product.refresh_from_db()

        self.assertEqual(self.product.name, data['name'])
        self.assertEqual(self.product.description, data['description'])

    def test_update_nonexistent_product(self):
        # Arrange
        non_existent_id = 999
        url = reverse(
            'product-detail',
            kwargs={'pk': non_existent_id}
        )
        data = {
            "name": "Nonexistent Product",
            "description": "This product does not exist."
        }

        # Act
        response = self.client.patch(
            url,
            data,
            format='json'
        )

        # Assert
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_delete_product(self):
        # Act
        response = self.client.delete(self.product_detail_url)

        # Assert
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertTrue(Product.objects.filter(id=self.product.id).exists())
        self.product.refresh_from_db()
        self.assertTrue(self.product.deleted)


class SizeManagementTests(APITestCase):

    def setUp(self):
        self.size = Size.objects.create(name="Large")

        self.size_list_url = reverse('size-list')
        self.size_detail_url = reverse(
            'size-detail',
            kwargs={'pk': self.size.id}
        )

    # -------------------------
    # GET TESTS
    # -------------------------

    def test_get_all_sizes(self):
        response = self.client.get(self.size_list_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data), 1)
        self.assertEqual(response.data[0]['name'], "Large")

    def test_get_size_by_id(self):
        response = self.client.get(self.size_detail_url)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['id'], self.size.id)
        self.assertEqual(response.data['name'], "Large")

    # -------------------------
    # POST TESTS
    # -------------------------

    def test_create_size(self):
        data = {
            "name": "Medium"
        }

        response = self.client.post(
            self.size_list_url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['name'], "Medium")
        self.assertTrue(
            Size.objects.filter(name="Medium").exists()
        )

    def test_create_size_with_duplicate_name(self):
        data = {
            "name": "Large"
        }

        response = self.client.post(
            self.size_list_url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_size_with_empty_name(self):
        data = {
            "name": "   "
        }

        response = self.client.post(
            self.size_list_url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    # -------------------------
    # PUT TESTS
    # -------------------------

    def test_update_size(self):
        data = {
            "name": "Extra Large"
        }

        response = self.client.put(
            self.size_detail_url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Extra Large")

        self.size.refresh_from_db()
        self.assertEqual(self.size.name, "Extra Large")

    # -------------------------
    # PATCH TESTS
    # -------------------------

    def test_partial_update_size(self):
        data = {
            "name": "Small"
        }

        response = self.client.patch(
            self.size_detail_url,
            data,
            format='json'
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], "Small")

        self.size.refresh_from_db()
        self.assertEqual(self.size.name, "Small")

