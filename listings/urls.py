from django.urls import path
from . import views

app_name = 'listings'
urlpatterns = [
    path('',                             views.home,             name='home'),
    path('carte/',                       views.listing_map,      name='map'),
    path('api/geojson/',                 views.listings_geojson, name='geojson'),
    path('annonces/<int:pk>/',           views.listing_detail,   name='detail'),
    path('annonces/publier/',            views.listing_create,   name='create'),
    path('annonces/<int:pk>/modifier/',  views.listing_edit,     name='edit'),
    path('annonces/<int:pk>/supprimer/', views.listing_delete,   name='delete'),
    path('mes-annonces/',                views.my_listings,      name='my_listings'),
    path('favoris/',                     views.favorites,        name='favorites'),
    path('favoris/<int:pk>/',            views.toggle_favorite,  name='toggle_favorite'),
    path('health/',                      views.health_check,     name='health'),
]
