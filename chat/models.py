from django.db import models
from account.models import *
from courses.models import *
# Create your models here.
class ChatRoom(models.Model):
    name = models.CharField(max_length=100)
    users = models.ManyToManyField(UserAccount, related_name='chat_rooms')
    def __str__(self):
        return self.name
        

class ChatMessage(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(UserAccount, on_delete=models.CASCADE, related_name='sent_messages')
    message = models.TextField()
    time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.sender.username}: {self.message}'