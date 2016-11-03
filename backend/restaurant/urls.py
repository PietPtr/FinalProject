from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.login_view, name='login'),
    url(r'^checkurl$', views.checkurl, name='checkurl'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^cook$', views.cook, name='cook'),
    url(r'^verify$', views.verify, name='verify'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^menu$', views.menu, name='menu'),
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
