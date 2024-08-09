from django.contrib import admin

from ..models.student import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('individual', )
