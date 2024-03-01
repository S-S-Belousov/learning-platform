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


class ProductViewSet(viewsets.ModelViewSet):
    queryset = Product.objects.all()
    serializer_class = ProductSerializer


class LessonViewSet(viewsets.ModelViewSet):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer


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
