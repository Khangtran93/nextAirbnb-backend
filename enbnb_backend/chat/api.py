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
def get_conversation_details(request, pk):
  print("====pk in get messages====", pk)
  try:
    conversation = Conversation.objects.get(pk=pk)
    # messages = conversation.messages.all()
    serializer = ConversationDetailSerializer(conversation, many=False)
  except Conversation.DoesNotExist:
    return JsonResponse({'error': 'Conversation not found'}, status=404)
  return JsonResponse({'data': serializer.data})

@api_view(['GET'])
def conversation_start(request, landlord_id):
  print("======getting conversation id =====")
  if request.user.id == landlord_id:
    return JsonResponse({'error': 'You cannot start a conversation with yourself'}, status=400)
  try:
    conversation = Conversation.objects.all().filter(users__in=[request.user.id]).filter(users__in=[landlord_id]).first()
    if not conversation: 
      landlord = User.objects.get(id=landlord_id)
      conversation = Conversation.objects.create()
      conversation.users.add(request.user, landlord)
    return JsonResponse({'id': conversation.id})
  except Conversation.DoesNotExist:
    return JsonResponse({'error': 'Conversation not found'}, status=404)