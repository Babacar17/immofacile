from django.contrib import admin
from .models import Message, VisitRequest

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display  = ('sender','receiver','listing','status','created_at')
    list_filter   = ('status',)
    search_fields = ('sender__username','receiver__username','body')
    readonly_fields = ('created_at','read_at')

@admin.register(VisitRequest)
class VisitRequestAdmin(admin.ModelAdmin):
    list_display  = ('requester','listing','date','time_slot','status','created_at')
    list_filter   = ('status',)
    list_editable = ('status',)
    search_fields = ('requester__username','listing__title')
