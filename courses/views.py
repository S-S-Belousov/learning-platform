from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Lesson, Product
from .permissions import IsProductOwnerOrAdmin
from .serializers import (GroupSerializer, LessonSerializer, ProductSerializer,
                          ProductStatsSerializer)


class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductStatsSerializer


class BaseViewSet(viewsets.ModelViewSet):
    pass


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer
    permission_classes = [IsAuthenticated, IsProductOwnerOrAdmin]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        instance = serializer.instance
        instance.distribute_users_to_groups()
        headers = self.get_success_headers(serializer.data)
        return Response(
            serializer.data,
            status=status.HTTP_201_CREATED,
            headers=headers
            )


class LessonViewSet(BaseViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GroupViewSet(BaseViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer

    def perform_create(self, serializer):
        product_id = self.request.data.get('product_id')
        serializer.save(product_id=product_id)


class LogoutView(APIView):
    def post(self, request):
        try:
            token = Token.objects.get(user=request.user)
            token.delete()
        except Token.DoesNotExist:
            pass
        return Response(
            {'message': 'Successfully logged out'}, status=status.HTTP_200_OK
            )
