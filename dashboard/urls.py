from django.urls import path
from . import views
from AUTH_APP.views import * 

urlpatterns = [
    path('dashboard', views.dashboard, name='dashboard'),
    path('offre/modifier/<int:pk>/', views.modify_OffreDEmploi, name='modify_OffreDEmploi'),
    path('offre/supprimer/<int:pk>/', views.delete_OffreDEmploi, name='delete_OffreDEmploi'),
    path('dashboard_c', views.dashboard_c, name='dashboard_c'),
    path('demande/modifier/<int:pk>/', views.modify_DemandeDEmploi, name='modify_DemandeDEmploi'),
    path('demande/supprimer/<int:pk>/', views.delete_DemandeDEmploi, name='delete_DemandeDEmploi'),
]
