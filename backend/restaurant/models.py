from django.db import models


class Card(models.Model):
    identifier = models.IntegerField()

    def __str__(self):
        return str(self.id) + " : " + str(self.identifier)


class Account(models.Model):
    card = models.ForeignKey(Card)
    active = models.SmallIntegerField(default=0)
    paid = models.SmallIntegerField(default=0)

    def __str__(self):
        return str(self.id) + " : " + str(self.active) + " : " + str(self.paid)


class Food(models.Model):
    name = models.CharField(max_length=50)
    descr = models.CharField(max_length=150)
    price = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return str(self.name)


class Order(models.Model):
    account = models.ForeignKey(Account, null=True)
    food = models.ForeignKey(Food)
    done = models.SmallIntegerField(default=0)
    chrono = models.DateTimeField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return str(self.account) + " : " + str(self.food) + " : " + str(self.done) + " : " + str(self.chrono)


class CardSwipe(models.Model):
    identifier = models.AutoField(primary_key=True)
    card = models.ForeignKey(Card)
    device = models.CharField(max_length=50)


class Variables(models.Model):
    key = models.CharField(max_length=1024)
    value = models.CharField(max_length=1024)


class Permission(models.Model):
    class Meta:
        permissions = (
            ("isCook", "Can see the cooks page"),
            ("isWaiter", "Can see the waiter page"),
            ("isCashier", "Can see the cashier page"),
        )
