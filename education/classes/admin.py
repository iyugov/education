from django.contrib import admin

# Register your models here.

from .models import ClassGroup, ClassGroupEnrollment


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('grade', 'label')


@admin.register(ClassGroupEnrollment)
class ClassGroupEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group', 'enrollment_date')
