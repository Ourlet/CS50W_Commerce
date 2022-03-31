from traceback import print_exception
from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("create", views.create, name="create"),
    path("listing/<str:title>", views.listing, name="listing"),
    path("listing/<str:title>/add_watch", views.add_watchlist, name="add-watchlist"),
    path("listing/<str:title>/remove_watch", views.remove_watchlist, name="remove-watchlist"),
    path("listing/<str:title>/bid", views.bid, name="bid"),
    path("listing/<str:title>/close", views.close, name="close"),
    path("listing/<str:title>/comment", views.comment, name="comment"),
    path("watchlist", views.watchlist, name="watchlist"),
  
]


