from django.urls import path
from . import views

urlpatterns = [
    path('chat-landing/<str:user_name>/',views.chat_landing, name='Chat-Landing'),
    path('chat/<str:chat_name>/',views.chat, name='Chat'),
    path('dashboard/',views.dashboard, name='Dashboard'),
    path('search-users/', views.search_users, name='search_users'),
    
]

