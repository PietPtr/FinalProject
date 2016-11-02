from django.contrib import admin
from restaurant import models
from django.db import models

admin.site.register(models.Card)
admin.site.register(models.Food)
admin.site.register(models.Order)
admin.site.register(models.Account)
admin.site.register(models.CardSwipe)


class FoodAdmin(admin.ModelAdmin):
    list_display = (name)
