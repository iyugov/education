from django.contrib import admin

from ....entities.catalogs.transport_pass.models import TransportPass


@admin.register(TransportPass)
class TransportPassAdmin(admin.ModelAdmin):
    list_display = ('pass_id', )
    list_display_links = ('pass_id', )
    search_fields = ('pass_id', )
