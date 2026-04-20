from django.urls import path
from . import views
app_name = 'agencies'
urlpatterns = [
    path('',          views.agency_list,   name='list'),
    path('<int:pk>/', views.agency_detail, name='detail'),
]
