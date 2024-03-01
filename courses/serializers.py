from rest_framework import serializers

from .models import Group, Lesson, Product


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'


class GroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        fields = ['id', 'name']

    def create(self, validated_data):
        product_id = validated_data.pop('product_id', None)
        instance = super().create(validated_data)
        if product_id is not None:
            instance.product_id = product_id
            instance.save()
        return instance


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
        return obj.creator.groups_assigned.count()

    def get_group_fill_percentage(self, obj):
        total_students = obj.creator.groups_assigned.count()
        max_group_size = obj.max_group_size
        total_groups = obj.group_set.count()
        total_group_capacity = max_group_size * total_groups
        return (round(total_students / total_group_capacity * 100, 2)
                if total_group_capacity != 0 else 0)

    def get_product_purchase_percentage(self, obj):
        total_users = obj.creator.groups_assigned.count()
        access_count = obj.access_count()
        return (round(access_count / total_users * 100, 2)
                if total_users != 0 else 0)
