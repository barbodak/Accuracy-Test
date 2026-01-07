from django.db import models
from django.contrib.postgres.fields import ArrayField
from account.models import Account


class Quiztime(models.Model):
    """Stores timing information for quiz attempts"""

    start_time = models.DateTimeField(null=True, blank=True)
    finish_time = models.DateTimeField(null=True, blank=True)

    class Meta:
        verbose_name = "Quiz Time"
        verbose_name_plural = "Quiz Times"

    def __str__(self) -> str:
        return f"{self.start_time} → {self.finish_time}"

    @property
    def duration(self):
        """Calculate quiz duration"""
        if self.start_time and self.finish_time:
            return self.finish_time - self.start_time
        return None


class AcuTest_pic(models.Model):
    """Picture-based Acuity Test results"""

    # Use string reference to avoid circular imports
    account = models.ForeignKey(
        Account,
        on_delete=models.CASCADE,
        related_name="acutest_pics",
    )
    answers = ArrayField(models.IntegerField(), size=43)
    quiz_time = models.OneToOneField(
        Quiztime,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acutest_pic",
    )
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)  # Good to track

    class Meta:
        verbose_name = "Acuity Test (Picture)"
        verbose_name_plural = "Acuity Tests (Picture)"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        start = self.quiz_time.start_time if self.quiz_time else "N/A"
        return f"{self.account} | {start}"


class AcuTest_text(models.Model):
    """Text-based Acuity Test results"""

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="acutest_texts"
    )
    answers = ArrayField(models.IntegerField(), size=91)
    quiz_time = models.OneToOneField(
        Quiztime,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="acutest_text",
    )
    correct = models.IntegerField(default=0)
    wrong = models.IntegerField(default=0)
    num_of_yes = models.IntegerField(default=0)
    num_of_no = models.IntegerField(default=0)
    yes_yes = models.IntegerField(default=0)
    yes_no = models.IntegerField(default=0)
    no_no = models.IntegerField(default=0)
    no_yes = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Acuity Test (Text)"
        verbose_name_plural = "Acuity Tests (Text)"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        start = self.quiz_time.start_time if self.quiz_time else "N/A"
        return f"{self.account} | {start}"


class ValuTest(models.Model):
    """Values Test results"""

    account = models.ForeignKey(
        Account, on_delete=models.CASCADE, related_name="valutests"
    )
    answers = ArrayField(models.IntegerField(), size=30)
    quiz_time = models.OneToOneField(
        Quiztime,
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="valutest",
    )
    sharayet_kari = models.IntegerField(default=0)
    hemayat = models.IntegerField(default=0)
    ravabet = models.IntegerField(default=0)
    pishraft = models.IntegerField(default=0)
    esteghlal = models.IntegerField(default=0)
    tofigh = models.IntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        verbose_name = "Values Test"
        verbose_name_plural = "Values Tests"
        ordering = ["-created_at"]

    def __str__(self) -> str:
        start = self.quiz_time.start_time if self.quiz_time else "N/A"
        return f"{self.account} | {start}"
