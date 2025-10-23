from django.db import models
from django.contrib.auth.models import User
from django.db.models.enums import TextChoices
from django.utils.translation import gettext_lazy as _

from quiz.models import AcuTest_pic, AcuTest_text, Quiztime, ValuTest


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class Account(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    SEX_CHOICES = [  # Correct definition
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]

    # info
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    age = models.IntegerField(editable=True, null=True, blank=True)  # <-- CHANGED
    sex = models.CharField(
        max_length=1, choices=SEX_CHOICES, null=True, blank=True
    )  # <-- CHANGED (and removed duplicate)
    first_name = models.CharField(max_length=255, blank=True)  # <-- CHANGED
    last_name = models.CharField(max_length=255, blank=True)  # <-- CHANGED
    organization = models.ForeignKey(Organization, on_delete=models.DO_NOTHING)
    is_final = models.BooleanField(default=False)

    # quiz info
    acuTest_permition = models.BooleanField(editable=True, default=False)
    valTest_permition = models.BooleanField(editable=True, default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"


# Create your models here.
