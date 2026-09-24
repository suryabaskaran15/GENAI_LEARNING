from django.db import models


class Message(models.Model):
    ROLE_CHOICES = [
        ('user', 'user'),
        ('assistant', 'assistant'),
    ]

    conversation_id = models.CharField(max_length=100)  # groups messages into one conversation
    role = models.CharField(max_length=20, choices=ROLE_CHOICES)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)  # used to replay history in order

    class Meta:
        ordering = ['created_at']

    def __str__(self):
        return f'{self.conversation_id} [{self.role}]: {self.content[:30]}'
