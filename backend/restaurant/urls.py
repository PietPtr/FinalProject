from django.conf.urls import url

from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^waiter$', views.waiter, name='waiter'),
    url(r'^cashier$', views.cashier, name='cashier'),
]