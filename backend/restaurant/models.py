from django.db import models


class Card (models.Model):
    identifier = models.IntegerField()


class Account (models.Model):
    card = models.ForeignKey(Card)
    active = models.SmallIntegerField(default=0)
    payed = models.SmallIntegerField(default=0)


class Food (models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Order (models.Model):
    account = models.ForeignKey(Account)
    food = models.ForeignKey(Food)
    done = models.SmallIntegerField(default=0)


class CardSwipe (models.Model):
    card = models.ForeignKey(Card)
    device = models.CharField(max_length=50)
