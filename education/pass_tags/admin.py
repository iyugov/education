from django.contrib import admin

# Register your models here.

from .models import PassTag, PassTagRequest, PassTagRequestItem


class PassTagRequestItemInline(admin.TabularInline):
    model = PassTagRequestItem
    extra = 1


@admin.register(PassTag)
class PassCardAdmin(admin.ModelAdmin):
    list_display = ('tag_id', )
    list_display_links = ('tag_id', )
    search_fields = ('tag_id', )


@admin.register(PassTagRequest)
class PassTagRequestAdmin(admin.ModelAdmin):
    list_display = ('requester', 'executor', 'request_date', 'comment')
    list_display_links = ('requester', 'executor', 'request_date', 'comment')
    search_fields = ('requester', 'executor', 'request_date', 'comment')
    inlines = [PassTagRequestItemInline]


@admin.register(PassTagRequestItem)
class PassTagRequestItemAdmin(admin.ModelAdmin):
    list_display = ('pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status')
    list_display_links = ('pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status')
    search_fields = ('pass_tag_request', 'holder', 'reason', 'processing_date', 'pass_tag', 'status')
