from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class QuizInfo(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    start_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f'{self.user.username} : {self.start_time}'


class AcuTest(models.Model):
    answers = ArrayField(models.IntegerField(), max_length=43)
    quiz_info = models.OneToOneField(QuizInfo, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return f'{self.quiz_info.user.username} | {self.quiz_info.start_time}'


class ValuTest(models.Model):
    answers = ArrayField(models.IntegerField(), max_length=30)
    quiz_info = models.OneToOneField(QuizInfo, on_delete=models.CASCADE)
    sharayet_kari = models.IntegerField()
    hemayat = models.IntegerField()
    ravabet = models.IntegerField()
    pishraft = models.IntegerField()
    esteghlal = models.IntegerField()
    tofigh = models.IntegerField()

    def __str__(self) -> str:
        return f'{self.quiz_info.user.username} | {self.quiz_info.start_time}'
