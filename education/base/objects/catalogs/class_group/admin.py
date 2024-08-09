from django.contrib import admin

from ....objects.catalogs.class_group.models import ClassGroup


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('grade', 'label')
