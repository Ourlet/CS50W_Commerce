from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse

from .models import User, Listing, Bid, Comment, Watchlist


def index(request):
    return render(request, "auctions/index.html",{
        "listings" : Listing.objects.all() 
    })


def login_view(request):
    if request.method == "POST":

        # Attempt to sign user in
        username = request.POST["username"]
        password = request.POST["password"]
        user = authenticate(request, username=username, password=password)

        # Check if authentication successful
        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse("index"))
        else:
            return render(request, "auctions/login.html", {
                "message": "Invalid username and/or password."
            })
    else:
        return render(request, "auctions/login.html")


def logout_view(request):
    logout(request)
    return HttpResponseRedirect(reverse("index"))


def register(request):
    if request.method == "POST":
        username = request.POST["username"]
        email = request.POST["email"]

        # Ensure password matches confirmation
        password = request.POST["password"]
        confirmation = request.POST["confirmation"]
        if password != confirmation:
            return render(request, "auctions/register.html", {
                "message": "Passwords must match."
            })

        # Attempt to create new user
        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, "auctions/register.html", {
                "message": "Username already taken."
            })
        login(request, user)
        return HttpResponseRedirect(reverse("index"))
    else:
        return render(request, "auctions/register.html")

def create(request):
    # Identify the person logged as seller
    seller = request.user

    # Retrieve data from the Front End
    if request.method == "POST":
        title = request.POST["title"]
        description = request.POST["description"]
        price = request.POST["price"]
        category = request.POST["category"]
        image = request.POST["image"] 

        # Add the new listing in the Database
        Listing(title=title, description=description, price=price, image=image, category=category, seller=seller).save()
    
    return HttpResponseRedirect(reverse("index"))

def listing(request, title):

    listing = get_object_or_404(Listing, title=title)
    comments = listing.items.all()
    
    watchlisted = Watchlist.objects.filter(watcher = request.user)
    print(watchlisted)
    print(watchlisted.filter(watch_listing = listing))
    #if watchlisted.filter(watch_listing = listing) == None:
    #    watchlist = False
    #else :
    #    watchlist = True

    return render(request, "auctions/listing.html",{
        "title" : title,
        "listing" : listing,
        "comments": comments,
        #"watchlist" : watchlist
    })

def add_watchlist(request, title):
    return HttpResponseRedirect(reverse("listing", args=(title,)))

def remove_watchlist(request, title):
    return HttpResponseRedirect(reverse("listing", args=(title,)))
