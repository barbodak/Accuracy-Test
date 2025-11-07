from django.contrib import admin
from . import models


class ValuTestAdmin(admin.ModelAdmin):
    readonly_fields = (
        "sharayet_kari",
        "hemayat",
        "ravabet",
        "pishraft",
        "esteghlal",
        "tofigh",
    )


# Register your models here.
admin.site.register(models.Quiztime)
admin.site.register(models.AcuTest_pic)
admin.site.register(models.AcuTest_text)
admin.site.register(models.ValuTest, ValuTestAdmin)
