from django.contrib import admin

from ....entities.catalogs.pass_tag.models import PassTag


@admin.register(PassTag)
class PassTagAdmin(admin.ModelAdmin):
    list_display = ('tag_id', )
    list_display_links = ('tag_id', )
    search_fields = ('tag_id', )
