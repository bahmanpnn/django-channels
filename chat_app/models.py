# from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.db import models

user = get_user_model()


class Message(models.Model):
    # author = models.ForeignKey(User, on_delete=models.CASCADE)
    author = models.ForeignKey(user, on_delete=models.CASCADE)
    content = models.TextField()
    message_time = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.author.username}-{self.content}'

    def last_message(self):
        return Message.objects.order_by('-message_time').all()
