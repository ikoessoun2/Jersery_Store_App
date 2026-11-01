from django.shortcuts import render
from rest_framework.viewsets import ModelViewSet


from rest_framework import status, viewsets
from rest_framework.response import Response

from .serializers import CategorySerializer, ProductSerializer
from .services import CategoryService, ProductService
from .exceptions import ResourceNotFoundException

class CategoryViewSet(viewsets.ViewSet):

    def list(self, request):
        categories = CategoryService.get_all_categories()
        serializer = CategorySerializer(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        category = CategoryService.get_category_by_id(pk)
        serializer = CategorySerializer(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            serializer = CategorySerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            category = CategoryService.create_category(
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )

            response_serializer = CategorySerializer(category)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except Exception as e:
            return Response(
                {"detail": "category with this name already exists."},
                status=status.HTTP_409_CONFLICT
            )

    def update(self, request, pk=None):
        serializer = CategorySerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category_id=pk,
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description', '')
        )

        response_serializer = CategorySerializer(category)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        serializer = CategorySerializer(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category_id=pk,
            name=serializer.validated_data.get('name', None),
            description=serializer.validated_data.get('description', None)
        )

        response_serializer = CategorySerializer(category)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        CategoryService.delete_category(category_id=pk)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ViewSet):
    def list(self, request):
        products = ProductService.get_all_products()
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(pk)
        serializer = ProductSerializer(product)
        if product is None:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            serializer = ProductSerializer(data=request.data)
            serializer.is_valid(raise_exception=True)

            product = ProductService.create_product(
                category_id=serializer.validated_data['category'].id,
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )

            response_serializer = ProductSerializer(product)

            return Response(
                response_serializer.data,
                status=status.HTTP_201_CREATED
            )
        except ResourceNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


    def partial_update(self, request, pk=None):
        try:
            serializer = ProductSerializer(
                data=request.data,
                partial=True
            )
            serializer.is_valid(raise_exception=True)

            validated_data = serializer.validated_data

            product = ProductService.update_product(
                product_id=pk,
                category=validated_data.get('category'),
                name=validated_data.get('name'),
                description=validated_data.get('description')
            )

            response_serializer = ProductSerializer(product)

            return Response(
                response_serializer.data,
                status=status.HTTP_200_OK
            )

        except ResourceNotFoundException as e:
            return Response(
                {"detail": str(e)},
                status=status.HTTP_404_NOT_FOUND
            )


    def destroy(self, request, pk=None):
        ProductService.delete_product(product_id=pk)

        return Response(status=status.HTTP_204_NO_CONTENT)