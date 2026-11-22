from rest_framework import status, viewsets
from rest_framework.response import Response
from rest_framework.exceptions import ValidationError, NotFound
from rest_framework.permissions import AllowAny


from .serializers import CategorySerializer, ProductSerializer, SizeSerializer, ProductVariantSerializer, ProductImageSerializer
from .services import CategoryService, ProductService, SizeService, ProductVariantService, ProductImageService
from .exceptions import ResourceNotFoundException

class CategoryViewSet(viewsets.ViewSet):
    lookup_value_regex = r"\d+"
    serializer_class = CategorySerializer
    permission_classes = [AllowAny]

    def list(self, request):
        categories = CategoryService.get_all_categories()
        serializer = self.serializer_class(categories, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        category = CategoryService.get_category_by_id(pk)
        serializer = self.serializer_class(category)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            category = CategoryService.create_category(
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )

            response_serializer = self.serializer_class(category)

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
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category_id=pk,
            name=serializer.validated_data['name'],
            description=serializer.validated_data.get('description', '')
        )

        response_serializer = self.serializer_class(category)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        serializer = self.serializer_class(data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)

        category = CategoryService.update_category(
            category_id=pk,
            name=serializer.validated_data.get('name', None),
            description=serializer.validated_data.get('description', None)
        )

        response_serializer = self.serializer_class(category)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        CategoryService.delete_category(category_id=pk)

        return Response(status=status.HTTP_204_NO_CONTENT)


class ProductViewSet(viewsets.ViewSet):
    lookup_value_regex = r"\d+"
    serializer_class = ProductSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        products = ProductService.get_all_products()
        serializer = self.serializer_class(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        product = ProductService.get_product_by_id(pk)
        serializer = self.serializer_class(product)
        if product is None:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND
            )
        

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        try:
            serializer = self.serializer_class(data=request.data)
            serializer.is_valid(raise_exception=True)

            product = ProductService.create_product(
                category_id=serializer.validated_data['category'].id,
                name=serializer.validated_data['name'],
                description=serializer.validated_data.get('description', '')
            )

            response_serializer = self.serializer_class(product)

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
            serializer = self.serializer_class(
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

            response_serializer = self.serializer_class(product)

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


class SizeViewSet(viewsets.ViewSet):
    lookup_value_regex = r"\d+"
    serializer_class = SizeSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        sizes = SizeService.get_all_sizes()
        serializer = self.serializer_class(sizes, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        size = SizeService.get_size_by_id(pk)
        serializer = self.serializer_class(size)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.serializer_class(data=request.data)
        serializer.is_valid(raise_exception=True)

        size = SizeService.create_size(
            name=serializer.validated_data['name']
        )

        return Response(
            self.serializer_class(size).data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        existing_size = SizeService.get_size_by_id(pk)

        serializer = self.serializer_class(
            existing_size,
            data=request.data
        )
        serializer.is_valid(raise_exception=True)

        size = SizeService.update_size(
            size_id=pk,
            name=serializer.validated_data['name']
        )

        return Response(
            self.serializer_class(size).data,
            status=status.HTTP_200_OK
        )

    def partial_update(self, request, pk=None):
        existing_size = SizeService.get_size_by_id(pk)

        serializer = self.serializer_class(
            existing_size,
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        size = SizeService.update_size(
            size_id=pk,
            name=serializer.validated_data.get(
                'name', existing_size.name
            )
        )

        return Response(
            self.serializer_class(size).data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, pk=None):
        SizeService.delete_size(pk)

        return Response(status=status.HTTP_204_NO_CONTENT)




class ProductVariantViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r"\d+"
    queryset = ProductVariantService.get_all_product_variants()
    serializer_class = ProductVariantSerializer
    permission_classes = [AllowAny]

    def list(self, request):
        variants = ProductVariantService.get_all_product_variants()
        serializer = self.get_serializer(variants, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def retrieve(self, request, pk=None):
        try:
            variant = ProductVariantService.get_product_variant_by_id(pk)
        except ValueError as e:
            raise NotFound(str(e))

        serializer = self.get_serializer(variant)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def create(self, request):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            variant = ProductVariantService.create_product_variant(
                product_id=serializer.validated_data["product"].id,
                size_id=serializer.validated_data["size"].id,
                sku=serializer.validated_data["sku"],
                price=serializer.validated_data["price"]
            )
        except ValueError as e:
            raise ValidationError(str(e))

        response_serializer = self.get_serializer(variant)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, pk=None):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            variant = ProductVariantService.update_product_variant(
                variant_id=pk,
                **{
                    "product_id": serializer.validated_data["product"].id,
                    "size_id": serializer.validated_data["size"].id,
                    "sku": serializer.validated_data["sku"],
                    "price": serializer.validated_data["price"]
                }
            )
        except ValueError as e:
            raise ValidationError(str(e))

        response_serializer = self.get_serializer(variant)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def partial_update(self, request, pk=None):
        serializer = self.get_serializer(
            data=request.data,
            partial=True
        )
        serializer.is_valid(raise_exception=True)

        validated_data = serializer.validated_data

        update_data = {}

        if "product" in validated_data:
            update_data["product_id"] = validated_data["product"].id

        if "size" in validated_data:
            update_data["size_id"] = validated_data["size"].id

        if "sku" in validated_data:
            update_data["sku"] = validated_data["sku"]

        if "price" in validated_data:
            update_data["price"] = validated_data["price"]

        try:
            variant = ProductVariantService.update_product_variant(
                variant_id=pk,
                **update_data
            )
        except ValueError as e:
            raise ValidationError(str(e))

        response_serializer = self.get_serializer(variant)

        return Response(response_serializer.data, status=status.HTTP_200_OK)

    def destroy(self, request, pk=None):
        try:
            ProductVariantService.delete_product_variant(pk)
        except ValueError as e:
            raise NotFound(str(e))

        return Response(status=status.HTTP_204_NO_CONTENT)



class ProductImageViewSet(viewsets.ModelViewSet):
    lookup_value_regex = r"\d+"
    serializer_class = ProductImageSerializer
    queryset = ProductImageService.get_all_images()
    permission_classes = [AllowAny]

    def list(self, request, *args, **kwargs):
        images = self.queryset

        serializer = self.get_serializer(images, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def retrieve(self, request, *args, **kwargs):
        image = ProductImageService.get_image_by_id(
            kwargs.get("pk")
        )

        serializer = self.get_serializer(image)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK
        )

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        image = ProductImageService.create_image(
            serializer.validated_data
        )

        response_serializer = self.get_serializer(image)

        return Response(
            response_serializer.data,
            status=status.HTTP_201_CREATED
        )

    def update(self, request, *args, **kwargs):
        image_id = kwargs.get("pk")

        partial = kwargs.get("partial", False)

        serializer = self.get_serializer(
            data=request.data,
            partial=partial
        )

        serializer.is_valid(raise_exception=True)

        image = ProductImageService.update_image(
            image_id,
            serializer.validated_data
        )

        response_serializer = self.get_serializer(image)

        return Response(
            response_serializer.data,
            status=status.HTTP_200_OK
        )

    def destroy(self, request, *args, **kwargs):
        ProductImageService.delete_image(
            kwargs.get("pk")
        )

        return Response(
            status=status.HTTP_204_NO_CONTENT
        )
