from django.contrib import admin

# Register your models here.

from .models import PassTag, PassTagRequest


@admin.register(PassTag)
class PassCardAdmin(admin.ModelAdmin):
    list_display = ('tag_id', )
    list_display_links = ('tag_id', )
    search_fields = ('tag_id', )


@admin.register(PassTagRequest)
class PassCardIssueAdmin(admin.ModelAdmin):
    list_display = ('requester', 'executor', 'request_date', 'comment')
    list_display_links = ('requester', 'executor', 'request_date', 'comment')
    search_fields = ('requester', 'executor', 'request_date', 'comment')
