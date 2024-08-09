from django.contrib import admin

from ....objects.enums.gender.models import Gender


@admin.register(Gender)
class GenderAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )
