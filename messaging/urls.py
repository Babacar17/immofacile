from django.urls import path
from . import views
app_name = 'messaging'
urlpatterns = [
    path('',                                    views.inbox,               name='inbox'),
    path('envoyer/<int:listing_pk>/',           views.send_message,        name='send'),
    path('visite/<int:listing_pk>/',            views.request_visit,       name='visit_request'),
    path('mes-visites/',                        views.my_visits,           name='my_visits'),
    path('gerer-visites/',                      views.manage_visits,       name='manage_visits'),
    path('visite/<int:visit_pk>/<str:status>/', views.update_visit_status, name='update_visit'),
]
