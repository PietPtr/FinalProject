from django.shortcuts import render
from django.http import HttpResponse


def index(request):
    return HttpResponse("Index")


def waiter(request):
    return HttpResponse("waiter")


def cashier(request):
    return HttpResponse("cashier")


def cardswiped(request):
    return HttpResponse("card swiped!")
