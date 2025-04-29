from django.db import models

class Chat(models.Model):
    created_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE, related_name='creator')
    participant = models.ForeignKey('core.Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    approved = models.BooleanField(default=False)

class Message(models.Model):
    created_by = models.ForeignKey('core.Profile', on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)
    content = models.CharField(max_length=1024)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
