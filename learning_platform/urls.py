from django.contrib import admin
from django.urls import include, path
from rest_framework import routers
from rest_framework.authtoken.views import obtain_auth_token

from courses.views import (GroupViewSet, LessonViewSet, LogoutView,
                           ProductStatsViewSet, ProductViewSet)

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet, basename='product')
router.register(r'lessons', LessonViewSet, basename='lesson')
router.register(r'groups', GroupViewSet, basename='group')
router.register(r'stats', ProductStatsViewSet, basename='stats')

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
]
