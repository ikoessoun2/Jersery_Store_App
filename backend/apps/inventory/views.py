# from django.shortcuts import render

# # Create your views here.

# from rest_framework import status, viewsets
# from rest_framework.response import Response
# from rest_framework.exceptions import NotFound, ValidationError

# from .serializer import InventorySerializer
# from .service import InventoryService


# class InventoryViewSet(viewsets.ViewSet):

#     def list(self, request):
#         inventory = InventoryService.get_all()
#         serializer = InventorySerializer(inventory, many=True)

#         return Response(serializer.data)

#     def retrieve(self, request, pk=None):
#         try:
#             inventory = InventoryService.get_by_id(pk)
#         except ValidationError as exc:
#             raise NotFound(detail=str(exc.detail))

#         serializer = InventorySerializer(inventory)

#         return Response(serializer.data)

#     def create(self, request):
#         serializer = InventorySerializer(data=request.data)
#         serializer.is_valid(raise_exception=True)

#         try:
#             inventory = InventoryService.create(
#                 variant_id=serializer.validated_data["variant"].id,
#                 quantity=serializer.validated_data["quantity"]
#             )
#         except ValidationError as exc:
#             raise ValidationError(detail=exc.detail)

#         response_serializer = InventorySerializer(inventory)

#         return Response(
#             response_serializer.data,
#             status=status.HTTP_201_CREATED
#         )
