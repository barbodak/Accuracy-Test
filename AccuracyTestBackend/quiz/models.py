from django.db import models
from django.contrib.auth.models import User
from django.contrib.postgres.fields import ArrayField


class Quiztime(models.Model):
    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    def __str__(self) -> str:
        return f"{self.start_time} : {self.finish_time}"


class AcuTest_pic(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = ArrayField(models.IntegerField(), max_length=43)
    quiz_time = models.OneToOneField(Quiztime, on_delete=models.DO_NOTHING)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} | {self.quiz_time.start_time}"


class AcuTest_text(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = ArrayField(models.IntegerField(), max_length=91)
    quiz_time = models.OneToOneField(Quiztime, on_delete=models.DO_NOTHING)
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    num_of_yes = models.IntegerField(default=0)
    num_of_no = models.IntegerField(default=0)
    yes_yes = models.IntegerField(default=0)
    yes_no = models.IntegerField(default=0)
    no_no = models.IntegerField(default=0)
    no_yes = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} | {self.quiz_time.start_time}"


class ValuTest(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    answers = ArrayField(models.IntegerField(), max_length=30)
    quiz_time = models.OneToOneField(Quiztime, on_delete=models.DO_NOTHING)
    sharayet_kari = models.IntegerField(default=0)
    hemayat = models.IntegerField(default=0)
    ravabet = models.IntegerField(default=0)
    pishraft = models.IntegerField(default=0)
    esteghlal = models.IntegerField(default=0)
    tofigh = models.IntegerField(default=0)

    def __str__(self) -> str:
        return f"{self.user.username} | {self.quiz_time.start_time}"
