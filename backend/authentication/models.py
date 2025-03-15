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
    chat = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages', null=
                             True)
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='messages', null=True)
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received', null=True)
    message = models.TextField(null=True)
    created_at = models.DateTimeField(auto_now_add=True, null=True)

    def save(self, *args, **kwargs):

        if self.chat and self.sender:
            if self.sender == self.chat.user1:
                self.receiver = self.chat.user2
            elif self.sender == self.chat.user2:
                self.receiver = self.chat.user1
        super(ChatMessage, self).save(*args, **kwargs)

    def __str__(self):
        return f"From {self.sender.username} to {self.receiver.username}: {self.message[:30]}"

    