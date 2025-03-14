from django.db import models
import uuid
from django.conf import settings
from useraccount.models import User
# Create your models here.

class Conversation(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  users = models.ManyToManyField(User, related_name="sender_conversations")
  created_at = models.DateTimeField(auto_now_add=True)
  modified_at = models.DateTimeField(auto_now=True)

class Message(models.Model):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  conversation = models.ForeignKey(Conversation, related_name="messages", on_delete=models.CASCADE)
  sender = models.ForeignKey(User, related_name="sent_messages", on_delete=models.CASCADE)
  receiver = models.ForeignKey(User, related_name="received_messages", on_delete=models.CASCADE)
  body = models.TextField(blank=True, null=True)
  created_at = models.DateTimeField(auto_now_add=True)