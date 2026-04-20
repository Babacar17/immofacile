from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/',      admin.site.urls),
    path('dashboard/',  include('dashboard.urls')),
    path('',            include('listings.urls')),
    path('accounts/',   include('accounts.urls')),
    path('agences/',    include('agencies.urls')),
    path('messages/',   include('messaging.urls')),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

admin.site.site_header = "ImmoFacile – Administration"
admin.site.site_title  = "ImmoFacile"
admin.site.index_title = "Tableau de bord"
