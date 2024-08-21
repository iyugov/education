from django.contrib import admin

from ....entities.catalogs.employee.models import Employee, PositionItem


class PositionItemInline(admin.TabularInline):
    model = PositionItem
    extra = 1


@admin.register(Employee)
class EmployeeAdmin(admin.ModelAdmin):
    list_display = ('employee', )


@admin.register(PositionItem)
class ContactInfoItemAdmin(admin.ModelAdmin):
    list_display = ('employee', 'position', 'is_main')
    list_display_links = ('employee', 'position', 'is_main')
    search_fields = ('employee', 'position', 'is_main')
