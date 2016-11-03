from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^setup$', views.setup, name='setup'),
    url(r'^waiter$', views.waiter, name='waiter'),
    url(r'^cleanitems$', views.cleanitems, name='cleanitems'),
    url(r'^addorder$', views.addorder, name='addorder'),
    url(r'^rmorder$', views.rmorder, name='rmorder'),
    url(r'^cashier$', views.cashier, name='cashier'),
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^cardswiped$', views.cardswiped, name='cardswiped'),
    url(r'^reset$', views.reset, name='reset'),

]
