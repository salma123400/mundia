from django.urls import path 
from . import views 
from .views import CustomLoginView

urlpatterns = [
    path('', views.home, name="home"),
    path('sign_upc', views.sign_upc, name="sign_upc"),
    path('sign_upr', views.sign_upr, name="sign_upr"),
    path('logout',views.logoutUser,name='logout'),
    path('login/',CustomLoginView.as_view(),name='login'),
    path('update_recruteur',views.update_recruteur,name='update_recruteur'),
    path('update_candidat',views.update_candidat,name='update_candidat'),
]