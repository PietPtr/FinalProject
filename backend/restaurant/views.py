from PIL import Image
from django.shortcuts import render, redirect
from django.http import HttpResponse
import json
import random

from django.template import loader
from django.views.decorators.csrf import csrf_exempt

from restaurant.models import Order, CardSwipe, Account, Food, Card


def index(request):
    return HttpResponse("Correct IP")


def setup(request):
    #init()
    #return HttpResponse(str(n))
    return HttpResponse("1526389563258964715965236589652856325698")


def favicon(request):
    response = HttpResponse(mimetype="image/ico")
    img = Image.open("templates/favicon.ico")
    img.save(response,'ico')
    return response


def stylesheet(request):
    template = loader.get_template("static/stylesheet.css")
    return HttpResponse(template.render(), content_type="text/css")


def waiter(request):
    foods = Food.objects.all().order_by('name')
    context = {'foods': foods}
    return render(request, "waiter.html", context)


def addorder(request):
    food = Food.objects.filter(name=request.GET["food"])[:1][0]
    print("Adding: " + request.GET["food"])
    order = Order(food=food)
    order.save()
    print("Added: " + request.GET["food"])
    return HttpResponse("Done!")


def rmorder(request):
    print("Removing: " + request.GET["food"])
    food = Food.objects.filter(name=request.GET["food"])[:1][0]
    order = Order.objects.filter(food=food)[:1][0]
    order.delete()
    print("Removed: " + request.GET["food"])
    return HttpResponse("Done!")


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
        context = {'id': 0, 'price': "0,00€"}
    return render(request, 'cashier.html', context)


def checkout(request):
    swipe = CardSwipe.objects.filter(card=request.GET["swipeid"])[:1][0]
    account = Account.objects.filter(card=swipe.card, active=1)
    orders = Order.objects.filter(account=account, done=0)
    account.paid = 1
    account.active = 0
    account.save()
    for order in orders:
        order.done = 1
        order.save()
    swipe.delete()
    return HttpResponse("checkout done!")


@csrf_exempt
def cardswiped(request):
    addmode = True
    obj = json.loads(request.body.decode('utf-8'))
    print("Card swiped:")
    print(obj["id"])
    print(obj["type"])
    cards = Card.objects.filter(identifier=obj["id"])
    if obj:
        if addmode:
            if not cards:
                newcard = Card(identifier=obj["id"])
                newcard.save()
                print("New")
            else:
                print("Not new")
        else:
            if obj["type"] == "waiter":
                account = Account.objects.filter(card=cards[0], active=1)[:1][0]
                orders = Order.objects.filter(account=None)
                for order in orders:
                    order.account = account
                    order.save()
            elif obj["type"] == "cashier":
                account = Account.objects.filter(card=Card.objects.filter(identifier=obj["id"])[0], active=1)
                if not account:
                    newaccount = Account(card=Card.objects.filter(identifier=obj["id"])[0], active=1)
                    newaccount.save()
                else:
                    swipe = CardSwipe(card=Card.objects.filter(identifier=obj["id"])[0], device=obj["type"])
                    swipe.save()
            else:
                print("Error 01")
    return HttpResponse("OK")


primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103, 107,
          109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223, 227, 229,
          233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]

EXPONENT = 17
SIZE_N = 128
MILLER_RABIN_ROUNDS = 40

primeP = 0
primeQ = 0
n = 0
phi = 0
d = 0


def millerrabinfase1(number):
    """ removes all numbers which are not prime, based on trial division """
    if number % 2 == 0:
        return False
    else:
        for i in range(0, len(primes)):
            if number % primes[i] == 0 and number != primes[i]:
                return False
    return True


def millerrabinfase2(number, rounds):
    """ Performs miller rabin rounds """
    if number % 2 == 0:
        return False
    s = 0
    d = number - 1
    while True:
        quotient, remainder = divmod(d, 2)
        if remainder == 1:
            break
        s += 1
        d = quotient

    def trymillerrabin(a):
        if modexp(a, d, number) == 1:
            return False
        for i in range(s):
            if modexp(a, 2 ** i * d, number) == number - 1:
                return False  # n might be prime
        return True  # n definitly not prime

    for i in range(rounds):
        a = random.randrange(2, number - 2)
        if trymillerrabin(a):
            return False
    return True

def isprime(number, rounds):
    """ First executes trial division based on lookup-table of primes, then performs miller rabin rounds"""
    if millerrabinfase1(number):
        if millerrabinfase2(number, rounds):
            return True
    return False


def genprime(bitsize, rounds):
    """ Generates a random prime, with atleast bitsize number of bits,
    and tests primality with isprimeComplex function"""
    q = random.randrange(2 ** bitsize, 2 ** (bitsize + 1))
    if q % 2 == 0:
        q += 1

    # there is no need to change to random primes
    # +2 is good enough, even though it has a bias to primes after a large gap
    while not isprime(q, rounds):
        q += 2
    return q


def extendedeuclidean(a, b):
    """ Performs extended euclidean algorithm """
    oldb = b
    olda = a
    x0, x1, y0, y1 = 1, 0, 0, 1
    while b != 0:
        q, a, b = a // b, b, a % b
        x0, x1 = x1, x0 - q * x1
        y0, y1 = y1, y0 - q * y1

    # makes sure the output of the function is positive / performs modulo function to make numbers positive
    x0 %= oldb
    y0 %= olda

    return a, x0, y0


def getdecryptionkey(e, phi):
    """ Gets the decryption key corresponding to the encryption key e, the euleur totient of n"""
    _, d, _ = extendedeuclidean(e, phi)
    return d


def modexp(a, b, n):
    """ calculate a^b mod n, python libery also has this function, but yeah"""
    i = 1
    accumulator = 1

    # array containing all the values of a**(2**i) mod n
    mods = [a % n]

    # calculate all modulo's off the power of 2's up to b
    while 2 ** i <= b:
        mods.append((mods[i - 1] ** 2) % n)
        i += 1

    # multiply all the modulo's needed to make the number n
    while b > 0:
        if b >= 2 ** i:
            b -= 2 ** i
            accumulator *= mods[i]
            accumulator %= n
        i -= 1
    return accumulator


def init():
    global primeP
    primeP = genprime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    global primeQ
    primeQ = genprime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    global phi
    phi = (primeP - 1) * (primeQ - 1)

    while phi % EXPONENT == 0:
        # print("phi is divisable by exponent, automatic retry")
        primeP = genprime(SIZE_N, MILLER_RABIN_ROUNDS)
        primeQ = genprime(SIZE_N, MILLER_RABIN_ROUNDS)
        phi = (primeP - 1) * (primeQ - 1)
    global n
    n = primeP * primeQ
    global d
    d = getdecryptionkey(EXPONENT, phi)


def decrypt(uid):
    message = modexp(uid, d, n)
    # remove first 8 and last 8 bits, which are random padding
    return message & 0xFFFF00
