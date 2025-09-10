from django.db import models
from django.utils import timezone


class ChatMessage(models.Model):
    message = models.TextField()
    response = models.TextField()
    created_at = models.DateTimeField(default=timezone.now)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message: {self.message[:50]}..."
