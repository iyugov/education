from django.contrib import admin

from ....entities.catalogs.position.models import Position


@admin.register(Position)
class PositionAdmin(admin.ModelAdmin):
    list_display = ('title', )
