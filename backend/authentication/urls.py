from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='Home'),
    path('authentication/', views.auth, name='Auth'),
    path('login/',views.user_login, name='User-Login'),
    path('register/',views.user_register, name='User-Register'),
    path('logout/',views.user_logout, name='User-Logout'),
    
]