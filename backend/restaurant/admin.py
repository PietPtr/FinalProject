from django.contrib import admin
from restaurant import models

admin.site.register(models.Card, models.CardAdmin)
admin.site.register(models.Food, models.FoodAdmin)
admin.site.register(models.Order, models.OrderAdmin)
admin.site.register(models.Account, models.AccountAdmin)
admin.site.register(models.CardSwipe, models.CardSwipeAdmin)
admin.site.register(models.Variables, models.VariablesAdmin)
