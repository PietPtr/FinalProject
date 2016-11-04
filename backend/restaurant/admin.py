from django.contrib import admin
from restaurant import models

# this file denotes which tables are going to be shown in the Administrators-interface
admin.site.register(models.Card, models.CardAdmin)
admin.site.register(models.Food, models.FoodAdmin)
admin.site.register(models.Order, models.OrderAdmin)
admin.site.register(models.Account, models.AccountAdmin)
admin.site.register(models.CardSwipe, models.CardSwipeAdmin)
admin.site.register(models.Variables, models.VariablesAdmin)
