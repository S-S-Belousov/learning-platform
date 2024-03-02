from django.contrib.auth.models import User
from django.db import models


def num_students(product):
    return product.group_set.aggregate(
        total_students=models.Count('students', distinct=True)
        )['total_students'] or 0


def group_fill_percentage(product):
    max_group_size = product.max_group_size
    total_groups = product.group_set.count()
    total_group_capacity = max_group_size * total_groups
    if total_group_capacity == 0:
        return 0
    total_students = num_students(product)
    return round(total_students / total_group_capacity * 100, 2)


def product_purchase_percentage(product):
    total_students = User.objects.count()
    if total_students == 0:
        return 0
    access_count = num_students(product)
    return round(access_count / total_students * 100, 2)


def access_count(product):
    total_students = num_students(product)
    max_group_size = product.max_group_size
    total_groups = product.group_set.count()
    total_group_capacity = max_group_size * total_groups
    product_purchase_percentage = round(
        total_students / User.objects.count() * 100, 2
        ) if User.objects.count() != 0 else 0
    group_fill_percentage = round(
        total_students / total_group_capacity * 100, 2
        ) if total_group_capacity != 0 else 0
    return {
        'num_students': total_students,
        'group_fill_percentage': group_fill_percentage,
        'product_purchase_percentage': product_purchase_percentage
    }
