from django.urls import path
from . import api

urlpatterns = [
  path('', api.get_conversations, name="api_properties_list"),
  path('<uuid:pk>/', api.get_messages, name="api_get_conversation_messages")
]