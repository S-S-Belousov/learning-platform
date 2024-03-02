from django.contrib.auth.models import User
from django.db import models

from .utils.calculations import (access_count, group_fill_percentage,
                                 num_students, product_purchase_percentage)
from .utils.helpers import distribute_users_to_groups_helper


class Product(models.Model):
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='created_products'
    )
    min_group_size = models.IntegerField()
    max_group_size = models.IntegerField()
    users_with_access = models.ManyToManyField(
        User, related_name='products_with_access', blank=True
    )

    def __str__(self):
        return self.name

    def distribute_users_to_groups(self):
        distribute_users_to_groups_helper(self)

    def access_count(self):
        return access_count(self)

    def num_students(self):
        return num_students(self)

    def group_fill_percentage(self):
        return group_fill_percentage(self)

    def product_purchase_percentage(self):
        return product_purchase_percentage(self)


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    title = models.CharField(max_length=100)
    video_url = models.URLField()

    def __str__(self):
        return self.title


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, null=True)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='groups_assigned')

    def __str__(self):
        return self.name
