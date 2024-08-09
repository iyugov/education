from django.contrib import admin

from ....objects.documents.class_group_enrollment.models import ClassGroupEnrollment, ClassGroupEnrollmentItem


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

