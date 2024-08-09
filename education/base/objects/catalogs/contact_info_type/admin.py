from django.contrib import admin

from ....objects.catalogs.contact_info_type.models import ContactInfoType


@admin.register(ContactInfoType)
class ContactInfoTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )
