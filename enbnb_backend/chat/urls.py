from django.urls import path
from . import api

urlpatterns = [
  path('', api.get_conversations, name="api_properties_list"),
  path('<uuid:pk>/', api.get_conversation_details, name="api_get_conversation_messages"),
  path('start/<uuid:landlord_id>/', api.conversation_start, name="api_conversation_start"),
]