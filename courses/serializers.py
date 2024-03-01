from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Product, Lesson, Group


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name', 'students']


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductStatsSerializer(serializers.ModelSerializer):
    num_students = serializers.SerializerMethodField()
    group_fill_percentage = serializers.SerializerMethodField()
    product_purchase_percentage = serializers.SerializerMethodField()
    groups = GroupSerializer(many=True, read_only=True)

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'num_students',
            'group_fill_percentage',
            'product_purchase_percentage',
            'groups'
            ]

    def get_num_students(self, obj):
        return obj.creator.student_set.count()

    def get_group_fill_percentage(self, obj):
        total_students = obj.creator.student_set.count()
        max_group_size = obj.max_group_size
        total_groups = obj.group_set.count()
        total_group_capacity = max_group_size * total_groups
        if total_group_capacity == 0:
            return 0
        return round(total_students / total_group_capacity * 100, 2)

    def get_product_purchase_percentage(self, obj):
        total_users = User.objects.count()
        if total_users == 0:
            return 0
        access_count = obj.access_count()
        return round(access_count / total_users * 100, 2)
