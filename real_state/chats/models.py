from uuid import uuid4

from chats.constants import ROLE_OPTIONS
from django.db import models
from users.models import User


class Chat(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Chat created by {self.user} at {self.created_at}"

    class Meta:
        ordering = ["created_at"]


class Message(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    chat = models.ForeignKey(Chat, on_delete=models.CASCADE)
    content = models.TextField()
    role = models.CharField(max_length=9, choices=ROLE_OPTIONS)
    created_at = models.DateTimeField(auto_now_add=True)

    objects = models.Manager()

    def __str__(self):
        return f"Message from {self.user} at {self.created_at}"

    class Meta:
        ordering = ["created_at"]
