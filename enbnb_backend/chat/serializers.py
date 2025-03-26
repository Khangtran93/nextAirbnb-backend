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

class ConversationDetailSerializer(serializers.ModelSerializer):
  print("Got ConversationDetailSerializer")
  users = serializers.SerializerMethodField()
  messages = serializers.SerializerMethodField()

  def get_messages(self, obj):
    messages = obj.messages.all()
    messages_serializer = MessageSerializer(messages, many=True)
    return messages_serializer.data

  def get_users(self, obj):
    users = obj.users.all()
    return UserDetailsSerializer(users, many=True).data
  
  class Meta:
    model = Conversation
    fields = ('id', 'users','messages')
class MessageSerializer(serializers.ModelSerializer):
  sender = UserDetailsSerializer(many=False)
  class Meta:
    model = Message
    fields = (
      # 'id',
      'conversation',
      'body',
      'sender',
      # 'receiver',
      'created_at',
    )