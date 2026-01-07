from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Account
from quiz.models import AcuTest_pic, AcuTest_text, Quiztime, ValuTest


@receiver(post_save, sender=Account)
def create_related_quizzes(sender, instance, created, **kwargs):
    """
    This function is called right after an Account object is saved.
    The 'created' flag is True only the very first time it's created.
    """
    if created:
        # This code will now only run ONCE when a new Account is made.
        if not ValuTest.objects.filter(account=instance).exists():
            q1 = Quiztime.objects.create()
            ValuTest.objects.create(account=instance, quiz_time=q1, answers=[0] * 30)

        if not AcuTest_pic.objects.filter(account=instance).exists():
            q1 = Quiztime.objects.create()
            q2 = Quiztime.objects.create()
            AcuTest_pic.objects.create(account=instance, quiz_time=q1, answers=[0] * 42)
            AcuTest_text.objects.create(
                account=instance, quiz_time=q2, answers=[0] * 90
            )
