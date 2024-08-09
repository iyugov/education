from django.contrib import admin

from ....objects.catalogs.student.models import Student


@admin.register(Student)
class StudentAdmin(admin.ModelAdmin):
    list_display = ('individual', )
