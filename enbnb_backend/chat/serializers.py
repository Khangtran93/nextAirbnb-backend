from rest_framework import serializers
from useraccount.serializers import UserDetailsSerializer
from .models import Conversation, Message

class ConversationListSerializer(serializers.ModelSerializer):
  # users = UserDetailsSerializer(many=True, read_only=True)
  sender = serializers.SerializerMethodField()
  receivers = serializers.SerializerMethodField()

  def get_sender(self, obj):
    request = self.context.get('request')
    user = request.user if request and request.user.is_authenticated else None
    if user:
      return UserDetailsSerializer(user, many=False).data
    return None
  
  def get_receivers(self, obj):
    request = self.context.get('request')
    user = request.user if request and request.user.is_authenticated else None
    if user:
      receivers = obj.users.all().exclude(id=user.id)
      return UserDetailsSerializer(receivers, many=True).data
  class Meta:
    model = Conversation
    fields = ('id', 'sender', 'receivers')

class MessageSerializer(serializers.ModelSerializer):
  sender = UserDetailsSerializer(many=False, read_only=True)
  receiver = UserDetailsSerializer(many=False, read_only=True)
  class Meta:
    model = Message
    fields = (
      'id',
      'conversation',
      'body',
      'sender',
      'receiver',
      'created_at',
    )