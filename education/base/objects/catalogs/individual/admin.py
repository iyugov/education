from django.contrib import admin

from ....objects.catalogs.individual.models import Individual, ContactInfoItem


class ContactInfoItemInline(admin.TabularInline):
    model = ContactInfoItem
    extra = 1


@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number', 'comment')
    list_display_links = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number', 'comment')
    search_fields = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number', 'comment')
    inlines = [ContactInfoItemInline]


@admin.register(ContactInfoItem)
class ContactInfoItemAdmin(admin.ModelAdmin):
    list_display = ('individual', 'contact_info_type', 'value')
    list_display_links = ('individual', 'contact_info_type', 'value')
    search_fields = ('individual', 'contact_info_type', 'value')
