import uuid

from django.conf import settings
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin, UserManager
from django.db import models

# from property.models import Property

class CustomUserManager(UserManager):
  def _create_user(self, name, email, password, **extra_fields):
    if not email:
      raise ValueError("You have not specified email address")
    
    email = self.normalize_email(email)
    user = self.model(email=email, name=name, **extra_fields)
    user.set_password(password)
    user.save(using=self.db)

    return user
  
  def create_user(self, name=None, email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", False)
    extra_fields.setdefault("is_superuser", False)
    return self._create_user(name, email, password, **extra_fields)
  
  def create_superuser(self,  name=None, email=None, password=None, **extra_fields):
    extra_fields.setdefault("is_staff", True)
    extra_fields.setdefault("is_superuser", True)
    return self._create_user(name, email, password, **extra_fields)

# class Favorite(models.Model):
#   id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
#   user = models.ForeignKey('useraccount.User', related_name='user_favorites', on_delete=models.CASCADE) 
#   property = models.ForeignKey('property.Property', on_delete=models.CASCADE)
  
#   class Meta:
#     unique_together = ('user', 'property')

class User(AbstractBaseUser, PermissionsMixin):
  id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
  email = models.EmailField(unique=True)
  name = models.CharField(max_length=255, blank=True, null=True)
  avatar = models.ImageField(upload_to='uploads/avatar')
  favorite = models.ManyToManyField('property.Property', related_name='favorite_by',blank=True)

  is_active = models.BooleanField(default=True)
  is_superuser = models.BooleanField(default=False)
  is_staff = models.BooleanField(default=False)

  created_at = models.DateTimeField(auto_now_add=True)
  deleted_at = models.DateTimeField(auto_now_add=True)
  last_login = models.DateTimeField(blank=True, null=True)

  objects = CustomUserManager()

  USERNAME_FIELD = 'email'
  EMAIL_FIELD = 'email'
  REQUIRED_FIELDS = ['name',]



