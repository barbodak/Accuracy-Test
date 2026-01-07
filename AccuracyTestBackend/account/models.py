from django.db import models
from django.contrib.auth.models import User


class Organization(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self) -> str:
        return f"{self.name}"


class Account(models.Model):
    MALE = "M"
    FEMALE = "F"
    OTHER = "O"
    SEX_CHOICES = [
        (MALE, "Male"),
        (FEMALE, "Female"),
        (OTHER, "Other"),
    ]

    DIPLOMA = "diploma"
    STUDENT = "student"
    BACHELOR = "bachelor"
    MASTERS = "masters"
    DOCTORATE = "doctorate"
    DEGREE_CHOICES = [
        (DIPLOMA, "Diploma"),
        (STUDENT, "Student"),
        (BACHELOR, "Bachelor"),
        (MASTERS, "Masters"),
        (DOCTORATE, "Doctorate"),
    ]

    # info
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name="account")
    age = models.IntegerField(editable=True, null=True, blank=True)
    sex = models.CharField(max_length=1, choices=SEX_CHOICES, null=True, blank=True)
    first_name = models.CharField(max_length=255, blank=True)
    last_name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(blank=True)
    phone = models.CharField(blank=True, null=True, max_length=255)
    university = models.CharField(max_length=255, blank=True)
    major = models.CharField(max_length=255, blank=True)
    degree = models.CharField(
        max_length=20, choices=DEGREE_CHOICES, null=True, blank=True
    )
    organization = models.ForeignKey(
        Organization,
        on_delete=models.SET_NULL,  # Better than DO_NOTHING
        null=True,
        blank=True,
        related_name="accounts",
    )
    is_final = models.BooleanField(default=False)

    # quiz permissions
    acuTest_permission = models.BooleanField(editable=True, default=False)
    valuTest_permission = models.BooleanField(editable=True, default=False)

    def __str__(self) -> str:
        return f"{self.first_name} {self.last_name}"
