from django.contrib import admin
from django.urls import path, include
from rest_framework import routers
from courses.views import ProductViewSet, LessonViewSet, GroupViewSet, LogoutView, ProductStatsViewSet
from rest_framework.authtoken.views import obtain_auth_token

router = routers.DefaultRouter()
router.register(r'products', ProductViewSet)
router.register(r'lessons', LessonViewSet)
router.register(r'groups', GroupViewSet)
router.register(r'stats', ProductStatsViewSet)

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/', include(router.urls)),
    path('api/login/', obtain_auth_token, name='api-login'),
    path('api/logout/', LogoutView.as_view(), name='api-logout'),
]
