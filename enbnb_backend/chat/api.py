from rest_framework.decorators import api_view, authentication_classes, permission_classes
from django.http import JsonResponse

from chat.models import Conversation
from chat.serializers import ConversationListSerializer, ConversationDetailSerializer
from useraccount.models import User

@api_view(['GET'])
def get_conversations(request):
  conversation = request.user.sender_conversations.all()
  serializer = ConversationListSerializer(conversation, context={'request': request}, many=True)
  print('serializer.data', serializer.data)

  return JsonResponse({'data': serializer.data})

@api_view(['GET'])
def get_messages(request, pk):
  print("====pk in get messages====", pk)
  try:
    conversation = Conversation.objects.get(pk=pk)
    # messages = conversation.messages.all()
    serializer = ConversationDetailSerializer(conversation, many=False)
  except Conversation.DoesNotExist:
    return JsonResponse({'error': 'Conversation not found'}, status=404)
  return JsonResponse({'data': serializer.data})