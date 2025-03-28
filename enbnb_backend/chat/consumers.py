import json
from pydoc import text 

from asgiref.sync import sync_to_async
from channels.generic.websocket import AsyncWebsocketConsumer

from chat.models import Message

class ChatConsumer(AsyncWebsocketConsumer):
  async def connect(self):
    self.room_name = self.scope['url_route']['kwargs']['room_name']
    self.room_group_name = 'chat_%s' % self.room_name

    await self.channel_layer.group_add(
      self.room_group_name,
      self.channel_name
    )

    await self.accept()
  
  async def receive(self, text_data):
    await self.receive_messages(text_data)

  async def disconnect(self, close_code):
    await self.channel_layer.group_discard(
      self.room_group_name,
      self.channel_name
    )

  # receive mesasages
  async def receive_messages(self, text_data):
    data = json.loads(text_data)
    conversation_id = data['data']['conversation_id']
    sender_id = data['data']['sender']['id']
    receiver_id = data['data']['receiver']['id']
    name = data['data']['sender']['name']
    body = data['data']['body']

    await self.channel_layer.group_send(
      self.room_group_name,
      {
        'type': 'chat_message',
        'conversation_id': conversation_id,
        'sender_id': sender_id,
        'receiver_id': receiver_id,
        'name': name,
        'body': body,
      }
    )

    await self.save_message(conversation_id, receiver_id, body)

  # send messages
  async def chat_message(self, event):
    conversation_id = event['conversation_id']
    sender_id = event['sender_id']
    receiver_id = event['receiver_id']
    name = event['name']
    body = event['body']

    await self.send(text_data=json.dumps({
      'type': 'chat_message',
      'conversation_id': conversation_id,
      'sender_id': sender_id,
      'receiver_id': receiver_id,
      'name': name,
      'body': body,
    }))

  @sync_to_async
  def save_message(self, conversation_id, receiver_id, body):
    user = self.scope['user']

    message = Message.objects.create(conversation_id=conversation_id, body=body, sender=user, receiver_id=receiver_id)