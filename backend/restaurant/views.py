from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
import json
import random

from django.views.decorators.csrf import csrf_exempt

from restaurant.models import Order, CardSwipe, Account, Food, Card, Variables


def index(request):
    # Default reply to let the client know that this is the correct server
    return HttpResponse("Correct IP")


def setup(request):
    # this needs to be called by any client to retrieve the key
    if getvalue("not firstrun") == "":
        setvalue("not firstrun", "false")
        # initialize the encryption-system
        init()
        print("Encryption Key: " + getvalue("n"))
    # send the key to the client
    # (this part is going to change)
    return HttpResponse(getvalue("n"))


def reset(request):
    """Make the user complete a captcha so the system doesn't get reset by accident"""
    # get the desired result in a variable
    variable = getvalue("reset")
    # get the user input
    userinput = request.GET.get("reset", "0")
    # check if the variable is unset or the entry was wrong
    if not variable or userinput != variable:
        # generate two random numbers between 1 and 15
        a, b = random.randint(1, 15), random.randint(1, 15)
        # store the result of their addition in the database
        setvalue("reset", a + b)
        # send both variables as a response
        return HttpResponse(str(a) + " : " + str(b))
    else:
        # if the varialble matches the userinput match, reset all tables
        for account in Account.objects.all():
            account.delete()
        for cardswipe in CardSwipe.objects.all():
            cardswipe.delete()
        for variable in Variables.objects.all():
            variable.delete()
        for order in Order.objects.all():
            order.delete()
        for card in Card.objects.all():
            card.delete()
        # send a confirmation message if everything worked out
        return HttpResponse("Deleted!")


def waiter(request):
    # get all foods from database
    foods = Food.objects.all().order_by('name')
    context = {'foods': foods}
    # and render them into the template
    return render(request, "waiter.html", context)


def cleanitems(request):
    # check if there is a swiped card in queue
    swipes = CardSwipe.objects.filter(device="waiter")
    if swipes:
        # remove the last cardswipe and tell the waiter-frontend to refresh
        swipe = swipes[0]
        swipe.delete()
        return HttpResponse("true", content_type="text/plain")
    else:
        return HttpResponse("false", content_type="text/plain")


def addorder(request):
    """This function is called, when the waiter adds an item to the checkout-list"""
    # get the food that was selected
    food = Food.objects.filter(name=request.GET["food"])[:1][0]
    print("Adding: " + request.GET.get("food"))
    # create a new order without an assigned account
    order = Order(food=food)
    order.save()
    print("Added: " + request.GET.get("food"))
    return HttpResponse("Done!")


def rmorder(request):
    """This function is called, when the waiter removes an item from the checkout-list"""
    print("Removing: " + request.GET.get("food"))
    # get the food that has been ordered and delete one order
    # (it doesn't matter which, since there is only one waiter that can have orders) of that food
    food = Food.objects.filter(name=request.GET.get("food"))[:1][0]
    order = Order.objects.filter(food=food)[:1][0]
    order.delete()
    print("Removed: " + request.GET.get("food"))
    return HttpResponse("Done!")


def cashier(request):
    # get all recent card-swipes
    swipes = (CardSwipe.objects.filter(device="cashier")[:1])
    # if there are any card-swipes
    if swipes:
        # get the first one
        swiped = swipes[0]
        # get the first (and probably only) swipe
        account = Account.objects.filter(card=swiped.card, active=1)
        # get the account that belongs to that swipe
        items = Order.objects.filter(account=account)
        # get all items that account has bought
        price = 0
        for item in items:
            # add up the price
            price += item.food.price
        # pack it into the context
        context = {'id': swiped.pk, 'items': items, 'price': price, 'doreload': False}
    else:
        # if there are no swipes, then just serve the page
        context = {'id': 0, 'price': "0,00€", 'doreload': True}
    # render the template
    return render(request, 'cashier.html', context)


def checkout(request):
    # this is called, when the pay-button is pressed
    print(request.GET.get("swipeid"))
    # get the swipe-object belonging to that swipeid
    swipe = CardSwipe.objects.filter(identifier=request.GET.get("swipeid"))[:1][0]
    # get the account which the order belongs to
    account = Account.objects.filter(card=swipe.card, active=1)[:1][0]
    # get the orders that account has made
    orders = Order.objects.filter(account=account, done=0)
    # set the new parameters and save it
    account.paid = 1
    account.active = 0
    account.save()
    # go through all orders
    for order in orders:
        # and mark them done
        order.done = 1
        order.save()
    # finally delete the swipe-object, so the job is done
    swipe.delete()
    return HttpResponseRedirect("cashier", False)


@csrf_exempt
def cardswiped(request):
    # if you want to introduce new cards to the system, you can change this to True
    # it should be False for normal operation
    addmode = False

    # get the data from the client and parse the json-data
    data = json.loads(request.body.decode('utf-8'))

    # print the information for debug-purposes
    print("Card swiped:")
    print(data["id"])
    print(data["type"])

    # get all the cards with this specific card-id from the system (expected is wither 1 or 0 entries)
    cards = Card.objects.filter(identifier=data["id"])
    # if the data-object has been correctly parsed
    if data:
        if addmode:
            # if the card is already known to the system, the cards-object will be empty and return False
            if not cards:
                # create a new card with the received identifier
                newcard = Card(identifier=data["id"])
                # and save it
                newcard.save()
                print("Card was unknown to the system and has been saved!")
            else:
                print("Card was already known to the system!")
        else:
            # if the system is not in addmode, add the already known card to a new CardSwipe-object,
            # which will later be processed by the webinterfaces
            swipe = CardSwipe(card=Card.objects.filter(identifier=data["id"])[0], device=data["type"])
            # and save it
            swipe.save()
            # we also get a list of possible accounts
            accounts = Account.objects.filter(card=cards[0], active=1)
            # if the source of the packet is a waiter, then
            if data["type"] == "waiter":
                # we know
                account = accounts[:1][0]
                # we also want to know what orders have no account assigned to it
                orders = Order.objects.filter(account=None)
                # assign the account to the new orders
                for order in orders:
                    order.account = account
                    order.save()
                print("Card has been swiped at the waiter-terminal to make an order!")
            elif data["type"] == "cashier":
                # if the card has been swiped as the cashier
                if not accounts:
                    # create a new account since the card has been picked up by a customer and
                    # is now going to be used
                    newaccount = Account(card=Card.objects.filter(identifier=data["id"])[0], active=1)
                    newaccount.save()
                    print("Card has been swiped at the cashier-terminal to activate a Card!")
                else:
                    print("Card has been swiped at the cashier-terminal to make a Payment and return the Card!")
            else:
                print("Packet contained an invalid type!")
    return HttpResponse("OK")


def getvalue(key):
    """gets a stored variable from the database or an empty string if there is no variable stored"""
    variable = Variables.objects.filter(key=key)
    # if the query returns something, then
    if variable:
        # return the value for the specific key
        return variable[0].value
    else:
        # return nothing
        return ""


def setvalue(key, value):
    """creates or changes a variable stored in the database"""
    variable = Variables.objects.filter(key=key)
    # check if a Variable with that key exists
    if not variable:
        # create a new variable
        variable = Variables(key=key, value=str(value))
    else:
        # select the first (only) object
        variable = variable[0]
        # update the existing variable
        variable.value = str(value)
    # save the variable in the database
    variable.save()
    return None


####################################################################################
#                                                                                  #
#  Everything below is belongs to the encryption and is still under construction.  #
#                                                                                  #
####################################################################################


def millerrabinfase1(number):
    """ removes all numbers which are not prime,based on trial division """
    primes = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29, 31, 37, 41, 43, 47, 53, 59, 61, 67, 71, 73, 79, 83, 89, 97, 101, 103,
              107, 109, 113, 127, 131, 137, 139, 149, 151, 157, 163, 167, 173, 179, 181, 191, 193, 197, 199, 211, 223,
              227, 229, 233, 239, 241, 251, 257, 263, 269, 271, 277, 281, 283, 293]

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
    EXPONENT = 17
    SIZE_N = 128
    MILLER_RABIN_ROUNDS = 40

    primep = genprime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    primeq = genprime(SIZE_N / 2, MILLER_RABIN_ROUNDS)
    phi = (primep - 1) * (primeq - 1)

    while phi % EXPONENT == 0:
        # print("phi is divisable by exponent, automatic retry")
        primep = genprime(SIZE_N, MILLER_RABIN_ROUNDS)
        primeq = genprime(SIZE_N, MILLER_RABIN_ROUNDS)
        phi = (primep - 1) * (primeq - 1)

    setvalue("n", primep * primeq)
    setvalue("d", getdecryptionkey(EXPONENT, phi))


def decrypt(uid):
    message = modexp(uid, int(getvalue("d")), int(getvalue("n")))
    # remove first 8 and last 8 bits, which are random padding
    return message & 0xFFFF00
