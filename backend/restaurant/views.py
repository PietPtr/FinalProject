from django.shortcuts import render, redirect
from django.http import HttpResponse
import json

from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from restaurant.models import Order, CardSwipe, Account, Food, Card


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
    swipes = (CardSwipe.objects.filter(device="cashier")[:1])
    if swipes:
        swiped = swipes[0]
        account = Account.objects.filter(card=swiped.card, active=1)
        items = Order.objects.filter(account=account)
        price = 0
        for item in items:
            price += item.food.price
        context = {'id': swiped.pk, 'items': items, 'price': price}
    else:
        context = {'price': "0,00€"}
    return render(request, 'cashier.html', context)


def checkout(request, swipeid):
    print(swipeid)
    return HttpResponse("checkout done!")


@csrf_exempt
def cardswiped(request):
    obj = json.loads(request.body.decode('utf-8'))
    if obj:
        print(obj["id"])
        swipe = CardSwipe(card=Card.objects.filter(identifier=obj["id"])[0], device=obj["type"])
        swipe.save()
    return HttpResponse("OK")
