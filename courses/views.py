from django.db.models import Count
from rest_framework import status, viewsets
from rest_framework.authtoken.models import Token
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Group, Lesson, Product
from .serializers import (GroupSerializer, LessonSerializer, ProductSerializer,
                          ProductStatsSerializer)


class ProductStatsViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Product.objects.annotate(
        num_students=Count('group__students')
        ).all()
    serializer_class = ProductStatsSerializer


class BaseViewSet(viewsets.ModelViewSet):
    pass


class ProductViewSet(BaseViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


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
