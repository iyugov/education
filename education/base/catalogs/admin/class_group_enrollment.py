from django.contrib import admin

# Register your models here.

from ..models.class_group_enrollment import ClassGroupEnrollment, ClassGroupEnrollmentItem, ClassGroupEnrollmentRegistryItem


class ClassGroupEnrollmentItemInline(admin.TabularInline):
    model = ClassGroupEnrollmentItem
    extra = 1


@admin.register(ClassGroupEnrollment)
class ClassGroupEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('enrollment_date', )


@admin.register(ClassGroupEnrollmentItem)
class ClassGroupEnrollmentItemAdmin(admin.ModelAdmin):
    list_display = ('class_group_enrollment', 'student', 'class_group')
    list_display_links = ('class_group_enrollment', 'student', 'class_group')
    search_fields = ('class_group_enrollment', 'student', 'class_group')


@admin.register(ClassGroupEnrollmentRegistryItem)
class ClassGroupEnrollmentRegistryItemAdmin(admin.ModelAdmin):
    list_display = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
    list_display_links = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
    search_fields = ('class_group_enrollment', 'enrollment_date', 'student', 'class_group')
