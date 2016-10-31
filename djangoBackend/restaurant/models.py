from django.db import models

# Create your models here.

class Card (models.Model):
    identifier = models.IntegerField()


class Account (models.Model):
    card = models.ForeignKey(Card)




class Food (models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2)


class Order (models.Models):
    account = models.ForeignKey(Account)
    food = models.ForeignKey(Food)
