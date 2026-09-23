from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('chat/', views.chat, name='chat'),  # frontend sends the user's message here
]
