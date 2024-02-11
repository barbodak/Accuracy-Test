from django.contrib import admin
from . import models


class ValuTestAdmin(admin.ModelAdmin):
    readonly_fields = ('sharayet_kari', 'hemayat', 'ravabet',
                       'pishraft', 'esteghlal', 'tofigh')


# Register your models here.
admin.site.register(models.QuizInfo)
admin.site.register(models.AcuTest)
admin.site.register(models.ValuTest, ValuTestAdmin)
