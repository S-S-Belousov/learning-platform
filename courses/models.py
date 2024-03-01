from math import ceil

from django.contrib.auth.models import AbstractUser
from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver


class User(AbstractUser):
    groups = models.ManyToManyField('auth.Group', related_name='courses_users')
    user_permissions = models.ManyToManyField(
        'auth.Permission', related_name='courses_users'
    )


class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)


class Product(models.Model):
    name = models.CharField(max_length=100)
    start_datetime = models.DateTimeField()
    cost = models.DecimalField(max_digits=10, decimal_places=2)
    creator = models.ForeignKey(
        UserProfile, on_delete=models.CASCADE, related_name='created_products'
        )
    min_group_size = models.IntegerField()
    max_group_size = models.IntegerField()

    def __str__(self):
        return self.name

    @transaction.atomic
    def distribute_users_to_groups(self):
        groups = self.group_set.all().order_by('id')
        num_groups = groups.count()
        if num_groups == 0:
            return
        students = self.creator.groups_assigned.all().order_by('id')
        num_students = students.count()
        min_group_size = self.min_group_size
        max_group_size = self.max_group_size
        ideal_group_size = ceil(num_students / num_groups)
        start_idx = 0
        for idx, group in enumerate(groups):
            end_idx = min(start_idx + ideal_group_size, num_students)
            group_size = min(max_group_size, end_idx - start_idx)
            if group_size < min_group_size:
                group_size = min_group_size
            group_students = students[start_idx:start_idx + group_size]
            group.students.set(group_students)
            start_idx += group_size
        groups[num_students:].delete()

    def access_count(self):
        return self.group_set.aggregate(
            total_students=models.Count(
                'students', distinct=True
            )
        )['total_students']


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


@receiver(post_save, sender=Product)
def distribute_users(sender, instance, **kwargs):
    instance.distribute_users_to_groups()
