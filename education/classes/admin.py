from django.contrib import admin

# Register your models here.

from .models import Student, ClassGroup, ClassGroupEnrollment


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('individual', )


@admin.register(ClassGroup)
class ClassGroupAdmin(admin.ModelAdmin):
    list_display = ('grade', 'label')


@admin.register(ClassGroupEnrollment)
class ClassGroupEnrollmentAdmin(admin.ModelAdmin):
    list_display = ('student', 'class_group', 'enrollment_date')
