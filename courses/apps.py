from django.apps import AppConfig
from django.db.models.signals import post_save
from django.dispatch import receiver


class CoursesConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'courses'

    def ready(self):
        from .models import Product

        @receiver(post_save, sender=Product)
        def distribute_users(sender, instance, **kwargs):
            instance.distribute_users_to_groups()
