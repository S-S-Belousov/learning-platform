from django.contrib import admin

from .models import Group, Lesson, Product


class ProductAdmin(admin.ModelAdmin):
    list_display = ['name', 'start_datetime', 'cost', 'creator']
    list_filter = ['start_datetime', 'creator']
    search_fields = ['name']


class LessonAdmin(admin.ModelAdmin):
    list_display = ['title', 'product', 'video_url']
    list_filter = ['product']
    search_fields = ['title']


class GroupAdmin(admin.ModelAdmin):
    list_display = ['name', 'product']
    list_filter = ['product']
    search_fields = ['name']


admin.site.register(Product, ProductAdmin)
admin.site.register(Lesson, LessonAdmin)
admin.site.register(Group, GroupAdmin)
