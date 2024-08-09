from django.contrib import admin

from ....objects.registries.class_group_enrollment_registry.models import ClassGroupEnrollmentRegistryItem


@admin.register(ClassGroupEnrollmentRegistryItem)
class ClassGroupEnrollmentRegistryItemAdmin(admin.ModelAdmin):
    list_display = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
    list_display_links = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
    search_fields = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
