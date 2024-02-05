from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from quiz.models import AcuTest, QuizInfo, ValuTest


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f'{self.name}'


class Account(models.Model):
    class Sex(models.TextChoices):
        MALE = "MALE ", _("MALE")
        FEMALE = "FEMALE ", _("FEMALE")
        __empty__ = _("(Unknown)")

    # info
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(editable=True)
    sex = models.TextField(choices=Sex, default=Sex.__empty__)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)

    # quiz info
    acuTest_permition = models.BooleanField(editable=True, default=False)
    valTest_permition = models.BooleanField(editable=True, default=False)

    def save(self, *args, **kwargs):
        if not ValuTest.objects.filter(quiz_info__user=self.user).exists():
            q1 = QuizInfo.objects.create(user=self.user)
            ValuTest.objects.create(quiz_info=q1, answers=[0] * 30)
        if not AcuTest.objects.filter(quiz_info__user=self.user).exists():
            q2 = QuizInfo.objects.create(user=self.user)
            AcuTest.objects.create(quiz_info=q2, answers=[0] * 30)
        super(Account, self).save(*args, **kwargs)

    def __str__(self) -> str:
        return f'{self.first_name} {self.last_name}'
# Create your models here.
