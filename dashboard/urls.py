from django.urls import path
from . import views

app_name = 'dashboard'

urlpatterns = [
    path('',                                    views.dashboard_home,        name='home'),
    path('utilisateurs/',                        views.user_list,             name='users'),
    path('utilisateurs/<int:pk>/',               views.user_detail,           name='user_detail'),
    path('utilisateurs/<int:pk>/activer/',       views.user_toggle_active,    name='user_toggle_active'),
    path('utilisateurs/<int:pk>/verifier/',      views.user_verify,           name='user_verify'),
    path('utilisateurs/<int:pk>/admin/',         views.user_make_staff,       name='user_make_staff'),
    path('utilisateurs/<int:pk>/supprimer/',     views.user_delete,           name='user_delete'),
    path('annonces/',                            views.listing_list,          name='listings'),
    path('annonces/<int:pk>/statut/',            views.listing_toggle_status, name='listing_status'),
    path('annonces/<int:pk>/vedette/',           views.listing_toggle_featured,name='listing_featured'),
    path('annonces/<int:pk>/supprimer/',         views.listing_delete,        name='listing_delete'),
    path('messages/',                            views.messages_list,         name='messages'),
    path('agences/',                             views.agencies_list,         name='agencies'),
    path('logs/',                                views.logs_view,             name='logs'),
    path('api/stats/',                           views.stats_json,            name='stats_json'),
]
