from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from django.template import loader

from restaurant.models import Order, CardSwipe, Account, Food


def index(request):
    return HttpResponse("Index")


def stylesheet(request):
    template = loader.get_template("stylesheet.css")
    return HttpResponse(template.render(), content_type="text/css")


def waiter(request):
    return HttpResponse("waiter")


def order(request):
    pass


def cashier(request):
    swiped = (CardSwipe.objects.filter(device="cashier")[:1])[0]
    if swiped:
        account = Account.objects.filter(card=swiped.card, active=1)
        items = Order.objects.filter(account=account)
        price = 0
        for item in items:
            price += item.food.price
        context = {'items': items, 'price': price}
    else:
        context = {'price': "0,00€"}
    return render(request, 'cashier.html', context)


def cardswiped(request):
    obj = json.loads(request.body)
    swipe = CardSwipe(card=obj["id"], device=obj["type"])
    swipe.save()
    return HttpResponse("")


def checkout(request):
    return HttpResponse("checkout done!")
