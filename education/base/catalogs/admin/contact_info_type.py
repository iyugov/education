from django.contrib import admin

from ..models.contact_info_type import ContactInfoType


@admin.register(ContactInfoType)
class ContactInfoTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )
