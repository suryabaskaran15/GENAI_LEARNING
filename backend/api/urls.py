from django.urls import path

from . import views

urlpatterns = [
    path('health/', views.health_check, name='health-check'),
    path('chat/', views.chat, name='chat'),  # frontend sends the user's message here
    path('learn/first-llm-api-call/', views.first_llm_api_call, name='learn-first-llm-api-call'),
    path('learn/context/', views.context_example, name='learn-context'),
    path('learn/instructions/', views.instructions_example, name='learn-instructions'),
    path('learn/conversation/', views.conversation_history_example, name='learn-conversation'),
    path('learn/stream/', views.stream_example, name='learn-stream'),
    path('learn/formatted-response/', views.formatted_response_example, name='learn-formatted-response'),
    path('learn/temperature/', views.temperature_example, name='learn-temperature'),
    path('learn/retries/', views.retries_example, name='learn-retries'),
]
