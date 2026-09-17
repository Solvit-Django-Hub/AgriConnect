from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Product
from .serializers import ProductSerializer


class ProductListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        products = Product.objects.all().order_by("-created_at")
        serializer = ProductSerializer(products, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        if request.user.role != "FARMER":
            return Response(
                {"detail": "Only farmers can create products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(data=request.data)

        if serializer.is_valid():
            product = serializer.save(farmer=request.user)

            return Response(
                ProductSerializer(product).data,
                status=status.HTTP_201_CREATED,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )


class ProductDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def get_product(self, product_id):
        try:
            return Product.objects.get(id=product_id)
        except Product.DoesNotExist:
            return None

    def put(self, request, product_id):
        product = self.get_product(product_id)

        if product is None:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "FARMER":
            return Response(
                {"detail": "Only farmers can update products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if product.farmer != request.user:
            return Response(
                {"detail": "You can only update your own products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(product, data=request.data)

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def patch(self, request, product_id):
        product = self.get_product(product_id)

        if product is None:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "FARMER":
            return Response(
                {"detail": "Only farmers can update products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if product.farmer != request.user:
            return Response(
                {"detail": "You can only update your own products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        serializer = ProductSerializer(
            product,
            data=request.data,
            partial=True,
        )

        if serializer.is_valid():
            serializer.save()

            return Response(
                serializer.data,
                status=status.HTTP_200_OK,
            )

        return Response(
            serializer.errors,
            status=status.HTTP_400_BAD_REQUEST,
        )

    def delete(self, request, product_id):
        product = self.get_product(product_id)

        if product is None:
            return Response(
                {"detail": "Product not found."},
                status=status.HTTP_404_NOT_FOUND,
            )

        if request.user.role != "FARMER":
            return Response(
                {"detail": "Only farmers can delete products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        if product.farmer != request.user:
            return Response(
                {"detail": "You can only delete your own products."},
                status=status.HTTP_403_FORBIDDEN,
            )

        product.delete()

        return Response(
            status=status.HTTP_204_NO_CONTENT,
)