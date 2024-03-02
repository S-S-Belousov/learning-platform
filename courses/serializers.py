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
            instance.product.distribute_users_to_groups()
        return instance


class ProductSerializer(serializers.ModelSerializer):
    class Meta:
        model = Product
        fields = '__all__'


class ProductStatsSerializer(serializers.ModelSerializer):
    num_students = serializers.IntegerField()
    group_fill_percentage = serializers.FloatField()
    product_purchase_percentage = serializers.FloatField()

    class Meta:
        model = Product
        fields = [
            'id',
            'name',
            'num_students',
            'group_fill_percentage',
            'product_purchase_percentage',
        ]
