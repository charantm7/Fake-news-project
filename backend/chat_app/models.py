from django.db import models
from django.contrib.auth import get_user_model
from django.db import models

User = get_user_model()

# Create your models here.

class ChatRoom(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats', null=True)
    name = models.CharField(max_length=100)
    user1 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_initiated', null=True)
    user2 = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_received', null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def __str__(self):
        return self.name
    
class ChatMessage(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='chats_user', null=True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sender", null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name="receiver", null=True)
    content = models.TextField(null=True)
    timestamp  = models.DateTimeField(auto_now_add=True, null=True)

    def __str__ (self):
        return f'{self.sender.username} -> {self.receiver.username} : {self.content[:20]}'

    