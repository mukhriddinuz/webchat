from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class User(AbstractUser):
   status = models.IntegerField(choices=((1, 'Admin'), (2, 'Employee')), default=1)
   image = models.ImageField(upload_to='users/', blank=True, null=True)


class Chat(models.Model):
   name = models.CharField(max_length=255, null=True)
   is_active = models.BooleanField(default=True)
   created_at = models.DateTimeField(auto_now_add=True)
   date = models.DateTimeField(auto_now=True)
   is_group = models.BooleanField(default=False)
   participants = models.ManyToManyField(User, related_name='chat_groups', verbose_name='ishtirokchilar')
   sender = models.ForeignKey(User, related_name='sender_chats', on_delete=models.SET_NULL, null=True, db_index=True, verbose_name='jonatuvchi')
   recipient = models.ForeignKey(User, related_name='recipient_chats', on_delete=models.SET_NULL, null=True, db_index=True, verbose_name='qabul qiluvchi')
   is_request = models.BooleanField(default=False)


class Message(models.Model):
   sender = models.ForeignKey(User, on_delete=models.SET_NULL, null=True, blank=True)
   created_at = models.DateTimeField(auto_now_add=True)
   chat = models.ForeignKey(Chat, on_delete=models.SET_NULL, null=True, blank=True)
   file = models.FileField(upload_to='message_files/', blank=True, null=True)
   text = models.TextField()
   is_main = models.BooleanField(default=False)
   is_edited = models.DateTimeField(auto_now=True)
   is_deleted = models.DateTimeField(null=True, blank=True)

   def soft_delete(self):
        self.is_deleted = timezone.now()
        self.save()
