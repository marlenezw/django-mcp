from django.urls import path
from . import views

app_name = 'chat'

urlpatterns = [
    path('', views.chat_view, name='index'),
    path('send/', views.send_message, name='send_message'),
    path('clear/', views.clear_chat, name='clear_chat'),
]
