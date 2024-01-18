from django.db import models
from django.contrib.auth.models import User


class QuizInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    start_time = models.DateTimeField()

    def __str__(self) -> str:
        return f'{self.user.username} : {self.start_time}'
