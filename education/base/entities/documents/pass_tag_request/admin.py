from django.contrib import admin

from ....entities.documents.pass_tag_request.models import PassTagRequest, PassTagRequestItem


class PassTagRequestItemInline(admin.TabularInline):
    model = PassTagRequestItem
    extra = 1


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
