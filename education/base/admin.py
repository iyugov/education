from django.contrib import admin

# Register your models here.

from .models import Individual, ContactInfoType, ContactInfoItem


class ContactInfoItemInline(admin.TabularInline):
    model = ContactInfoItem
    extra = 3


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
    list_display_links = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
    search_fields = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
    inlines = [ContactInfoItemInline]


@admin.register(ContactInfoType)
class ContactInfoTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )


@admin.register(ContactInfoItem)
class ContactInfoItemAdmin(admin.ModelAdmin):
    list_display = ('individual', 'contact_info_type', 'value')
    list_display_links = ('individual', 'contact_info_type', 'value')
    search_fields = ('individual', 'contact_info_type', 'value')
