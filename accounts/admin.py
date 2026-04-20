from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from .models import User

@admin.register(User)
class CustomUserAdmin(UserAdmin):
    list_display   = ('username','email','display_name','role','is_verified','date_joined')
    list_filter    = ('role','is_verified','is_active')
    search_fields  = ('username','email','first_name','last_name','agency_name')
    ordering       = ('-date_joined',)
    actions        = ['verify_users']
    fieldsets = UserAdmin.fieldsets + (
        ('ImmoFacile', {'fields': ('role','phone','whatsapp','avatar','bio','city','is_verified','notify_messages','notify_visits')}),
        ('Agence',     {'fields': ('agency_name','agency_address','agency_website','agency_license'), 'classes': ('collapse',)}),
    )

    @admin.action(description='Vérifier les comptes sélectionnés')
    def verify_users(self, request, queryset):
        updated = queryset.update(is_verified=True)
        self.message_user(request, f'{updated} compte(s) vérifié(s).')
