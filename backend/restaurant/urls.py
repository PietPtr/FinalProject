from django.conf.urls import url

from . import views

# this file denotes redirection-paths
# each category has a comment describing it's purpose

urlpatterns = [
    # authentication
    url(r'^$', views.login_view, name='login'),
    url(r'^checkurl$', views.checkurl, name='checkurl'),
    url(r'^login$', views.login_view, name='login'),
    url(r'^verify$', views.verify, name='verify'),
    url(r'^logout$', views.logout_view, name='logout'),
    url(r'^menu$', views.menu, name='menu'),

    # arduino interface
    url(r'^cardswiped$', views.cardswiped, name='cardswiped'),

    # waiter UI
    url(r'^waiter$', views.waiter, name='waiter'),
    url(r'^cleanitems$', views.cleanitems, name='cleanitems'),
    url(r'^addorder$', views.addorder, name='addorder'),
    url(r'^rmorder$', views.rmorder, name='rmorder'),

    # cashier UI
    url(r'^cashier$', views.cashier, name='cashier'),
    url(r'^checkout$', views.checkout, name='checkout'),
    url(r'^getbill$', views.getbill, name='getbill'),

    # cooks UI
    url(r'^cook$', views.cook, name='cook'),
    url(r'^confirmorder$', views.confirmorder, name='confirmorder'),

    # bookkeeping UI
    url(r'^bookkeeping$', views.bookkeeping, name='bookkeeping'),

    # maintainence and errorpages
    url(r'^reset$', views.reset, name='reset'),
    url(r'^error$', views.error, name='error'),

]
