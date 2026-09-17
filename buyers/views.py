from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from farmers.models import Product

from .serializers import BuyerProductSerializer


class BuyerProductListView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        if request.user.role != "BUYER":
            return Response(
                {"detail": "Only buyers can view products here."},
                status=status.HTTP_403_FORBIDDEN,
            )

        products = Product.objects.all().order_by("-created_at")
        serializer = BuyerProductSerializer(products, many=True)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )


class BuyerProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, product_id):
        if request.user.role != "BUYER":
            return Response(
                {"detail": "Only buyers can view product details here."},
                status=status.HTTP_403_FORBIDDEN,
            )

        try:
            product = Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        serializer = BuyerProductSerializer(product)

        return Response(
            serializer.data,
            status=status.HTTP_200_OK,
        )