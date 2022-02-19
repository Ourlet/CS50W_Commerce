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
    path("listing/<str:title>", views.add_watchlist, name="add-watchlist"),
    path("listing/<str:title>", views.remove_watchlist, name="remove-watchlist"),
]


