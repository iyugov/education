from django.contrib import admin

# Register your models here.

from .models import Individual

@admin.register(Individual)
class IndividualAdmin(admin.ModelAdmin):
    list_display = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
    list_display_links = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
    search_fields = ('last_name', 'first_name', 'patronymic', 'birth_date', 'social_insurance_number')
