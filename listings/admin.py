from django.contrib import admin
from .models import Listing, Photo, Favorite

class PhotoInline(admin.TabularInline):
    model  = Photo
    extra  = 1
    fields = ('image','caption','is_main','order')

@admin.register(Listing)
class ListingAdmin(admin.ModelAdmin):
    list_display    = ('title','type','city','price','status','owner','is_featured','views_count','created_at')
    list_filter     = ('type','status','city','furnished','is_featured')
    search_fields   = ('title','city','neighborhood','owner__username')
    list_editable   = ('status','is_featured')
    readonly_fields = ('views_count','created_at','updated_at','slug')
    inlines         = [PhotoInline]
    ordering        = ('-created_at',)
    fieldsets = (
        ('Général',       {'fields': ('owner','title','slug','description','type','status','is_featured')}),
        ('Localisation',  {'fields': ('country','city','neighborhood','address','latitude','longitude')}),
        ('Prix',          {'fields': ('price','price_charges','deposit','price_negotiable')}),
        ('Détails',       {'fields': ('surface','rooms','bedrooms','bathrooms','floor','available_from')}),
        ('Équipements',   {'fields': ('furnished','has_parking','has_wifi','has_ac','has_garden','has_pool','has_security','has_balcony','has_elevator','has_generator','has_water_tank','pets_allowed')}),
        ('Stats',         {'fields': ('views_count','created_at','updated_at'), 'classes': ('collapse',)}),
    )

@admin.register(Favorite)
class FavoriteAdmin(admin.ModelAdmin):
    list_display = ('user','listing','saved_at')
