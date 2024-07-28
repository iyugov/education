from django.contrib import admin

# Register your models here.

from .models import PassCardType, PassCardAction, PassCard, PassCardIssue


@admin.register(PassCardType)
class PassCardTypeAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )


@admin.register(PassCardAction)
class PassCardActionAdmin(admin.ModelAdmin):
    list_display = ('title', )
    list_display_links = ('title', )
    search_fields = ('title', )


@admin.register(PassCard)
class PassCardAdmin(admin.ModelAdmin):
    list_display = ('pass_id', 'pass_type')
    list_display_links = ('pass_id', 'pass_type')
    search_fields = ('pass_id', 'pass_type')


@admin.register(PassCardIssue)
class PassCardIssueAdmin(admin.ModelAdmin):
    list_display = ('issue_date', 'card', 'individual', 'description', 'action')
    list_display_links = ('issue_date', 'card', 'individual', 'description', 'action')
    search_fields = ('issue_date', 'card', 'individual', 'description', 'action')
