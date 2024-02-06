from django.contrib import admin
from . import models

# Register your models here.
admin.site.register(models.QuizInfo)
admin.site.register(models.AcuTest)
admin.site.register(models.ValuTest)
