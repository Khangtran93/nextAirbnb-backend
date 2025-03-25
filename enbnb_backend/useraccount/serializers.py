from dj_rest_auth.registration.serializers import RegisterSerializer
from rest_framework import serializers
from .models import User
from datetime import datetime

class CustomRegisterSerializer(RegisterSerializer):
    avatar = serializers.ImageField(required=False)  # Add avatar field
    name = serializers.CharField(required=True)

    def save(self, request):
        user = super().save(request)  # Call default user creation logic
        user.avatar = self.validated_data.get('avatar', None)  # Save avatar
        user.name = self.validated_data.get('name', None) #
        user.save()
        return user
class UserDetailsSerializer(serializers.ModelSerializer):
  year_experience = serializers.SerializerMethodField()

  def get_year_experience(self, obj):
    return (datetime.today().year + 1) - obj.created_at.year
  class Meta:
    model = User
    fields = (
      'id',
      'name',
      'email',
      'avatar',
      'year_experience'
    )