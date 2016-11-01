from django.contrib import admin
from restaurant import models

admin.site.register(models.Card)
admin.site.register(models.Food)
admin.site.register(models.Order)
