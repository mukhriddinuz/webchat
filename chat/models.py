from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
   status = models.IntegerField(choices=((1, 'Admin'), (2, 'Employee')), default=1)
   image = models.ImageField(upload_to='users/', blank=True, null=True)


class ChatGroup(models.Model):
   name = models.CharField(max_length=255)
   is_active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)
   date = models.DateTimeField(auto_now=True)
   users = models.ManyToManyField(User, related_name='chat_groups')


