from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
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


def login_view(request):
    return render(request, "login.html")


def verify(request):
    username = request.POST['username']
    password = request.POST['password']
    user = authenticate(username = username, password = password)
    if user is not None:
        login(request, user)
        return HttpResponseRedirect("menu")
    else:
        return render(request, "login.html", {"Error" : True})


def logout_view(request):
    logout(request)
    return render(request, "login.html", {"Logout": True})


@login_required
def menu(request):
    return render(request, "menu.html")


@login_required
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

@login_required
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
                # we know that the accounts-list contains exactly one item
                account = accounts[0]
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

sbox = {0x02, 0x03, 0x05, 0x07, 0x0B, 0x0D, 0x11, 0x13,
        0x17, 0x1D, 0x1F, 0x25, 0x29, 0x2B, 0x2F, 0x35,
        0x3B, 0x3D, 0x43, 0x47, 0x49, 0x4F, 0x53, 0x59,
        0x61, 0x65, 0x67, 0x6B, 0x6D, 0x71, 0x7F, 0x83,
        0x89, 0x8B, 0x95, 0x97, 0x9D, 0xA3, 0xA7, 0xAD,
        0xB3, 0xB5, 0xBF, 0xC1, 0xC5, 0xC7, 0xD3, 0xDF,
        0xE3, 0xE5, 0xE9, 0xEF, 0xF1, 0xFB, 0x01, 0x07,
        0x0D, 0x0F, 0x15, 0x19, 0x1B, 0x25, 0x33, 0x37,
        0x39, 0x3D, 0x4B, 0x51, 0x5B, 0x5D, 0x61, 0x67,
        0x6F, 0x75, 0x7B, 0x7F, 0x85, 0x8D, 0x91, 0x99,
        0xA3, 0xA5, 0xAF, 0xB1, 0xB7, 0xBB, 0xC1, 0xC9,
        0xCD, 0xCF, 0xD3, 0xDF, 0xE7, 0xEB, 0xF3, 0xF7,
        0xFD, 0x09, 0x0B, 0x1D, 0x23, 0x2D, 0x33, 0x39,
        0x3B, 0x41, 0x4B, 0x51, 0x57, 0x59, 0x5F, 0x65,
        0x69, 0x6B, 0x77, 0x81, 0x83, 0x87, 0x8D, 0x93,
        0x95, 0xA1, 0xA5, 0xAB, 0xB3, 0xBD, 0xC5, 0xCF,
        0xD7, 0xDD, 0xE3, 0xE7, 0xEF, 0xF5, 0xF9, 0x01,
        0x05, 0x13, 0x1D, 0x29, 0x2B, 0x35, 0x37, 0x3B,
        0x3D, 0x47, 0x55, 0x59, 0x5B, 0x5F, 0x6D, 0x71,
        0x73, 0x77, 0x8B, 0x8F, 0x97, 0xA1, 0xA9, 0xAD,
        0xB3, 0xB9, 0xC7, 0xCB, 0xD1, 0xD7, 0xDF, 0xE5,
        0xF1, 0xF5, 0xFB, 0xFD, 0x07, 0x09, 0x0F, 0x19,
        0x1B, 0x25, 0x27, 0x2D, 0x3F, 0x43, 0x45, 0x49,
        0x4F, 0x55, 0x5D, 0x63, 0x69, 0x7F, 0x81, 0x8B,
        0x93, 0x9D, 0xA3, 0xA9, 0xB1, 0xBD, 0xC1, 0xC7,
        0xCD, 0xCF, 0xD5, 0xE1, 0xEB, 0xFD, 0xFF, 0x03,
        0x09, 0x0B, 0x11, 0x15, 0x17, 0x1B, 0x27, 0x29,
        0x2F, 0x51, 0x57, 0x5D, 0x65, 0x77, 0x81, 0x8F,
        0x93, 0x95, 0x99, 0x9F, 0xA7, 0xAB, 0xAD, 0xB3,
        0xBF, 0xC9, 0xCB, 0xCF, 0xD1, 0xD5, 0xDB, 0xE7,
        0xF3, 0xFB, 0x07, 0x0D, 0x11, 0x17, 0x1F, 0x23,
        0x2B, 0x2F, 0x3D, 0x41, 0x47, 0x49, 0x4D, 0x53,
        }


def rotl(x):
    return (x << 1) | (x >> 7)


def rotr(x):
    return (x >> 1) | (x << 7)


def treyferdec(text):
    key = {0x12, 0x34, 0x56, 0x78, 0x9A, 0xBC, 0xDE, 0xFF}
    NUMROUNDS = 32

    for i in range(8 * NUMROUNDS - 1, 0, -1):
        t = text[i % 8]
        t += key[i % 8] % 256
        text[(i + 1) % 8] = rotr(text[(i + 1) % 8])
        text[(i + 1) % 8] = (text[(i + 1) % 8] - sbox[t]) % 256
    output = ''
    for i in range(3, 6, 1):
        output += text[i]
    return output
