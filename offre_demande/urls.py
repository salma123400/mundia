from django.urls import path 
from . import views
from AUTH_APP.views import * 

urlpatterns = [
    path('base', views.base, name="base"),
    path('offredemploi', views.offredemploi, name="offredemploi"),
]