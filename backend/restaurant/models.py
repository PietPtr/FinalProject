from django.contrib import admin
from django.db import models


class Card(models.Model):
    identifier = models.IntegerField()

    def __str__(self):
        return str(self.identifier)


class CardAdmin(admin.ModelAdmin):
    list_display = ('identifier',)


class Account(models.Model):
    card = models.ForeignKey(Card)
    active = models.SmallIntegerField(default=0)
    paid = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.id)


class AccountAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'active', 'paid',)


class Food(models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name)


class FoodAdmin(admin.ModelAdmin):
    list_display = ('name', 'descr', 'price',)


class Order(models.Model):
    account = models.ForeignKey(Account, null=True)
    food = models.ForeignKey(Food)
    done = models.SmallIntegerField(default=0)
    chrono = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.id)


class OrderAdmin(admin.ModelAdmin):
    list_display = ('account', 'food', 'done', 'chrono',)


class CardSwipe(models.Model):
    identifier = models.AutoField(primary_key=True)
    card = models.ForeignKey(Card)
    device = models.CharField(max_length=50)

    def __str__(self):
        return str(self.identifier)


class CardSwipeAdmin(admin.ModelAdmin):
    list_display = ('identifier', 'card', 'device',)


class Variables(models.Model):
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)

    def __str__(self):
        return str(self.key) + " = " + str(self.value)


class VariablesAdmin(admin.ModelAdmin):
    list_display = ('key', 'value',)


class Permission(models.Model):
    # Creates certain permissions to be linked to user accounts
    class Meta:
        permissions = (
            ("isCook", "Can see the cooks page"),
            ("isWaiter", "Can see the waiter page"),
            ("isCashier", "Can see the cashier page"),
            ("isBoss", "Can see the bookkeeping page"),
        )
