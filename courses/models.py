from math import ceil

from django.contrib.auth.models import User
from django.db import models, transaction


class Product(models.Model):
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(User, on_delete=models.CASCADE)
    min_group_size = models.IntegerField()
    max_group_size = models.IntegerField()

    def __str__(self):
        return self.name

    @transaction.atomic
    def distribute_users_to_groups(self):
        groups = self.group_set.all().order_by('id')
        num_groups = groups.count()
        num_students = User.objects.filter(
            groups_assigned__product=self
            ).count()
        min_group_size = self.min_group_size
        max_group_size = self.max_group_size
        ideal_group_size = ceil(num_students / num_groups)
        for idx, group in enumerate(groups):
            start_idx = idx * ideal_group_size
            end_idx = min(start_idx + ideal_group_size, num_students)
            group_size = min(max_group_size, end_idx - start_idx)
            if group_size < min_group_size:
                group_size = min_group_size
            students = self.students.all()[
                start_idx:start_idx + group_size
                ]
            group.students.set(students)
        groups[num_students:].delete()


class Lesson(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    video_url = models.URLField()

    def __str__(self):
        return self.title


class Group(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    students = models.ManyToManyField(User, related_name='groups_assigned')

    def __str__(self):
        return self.name
