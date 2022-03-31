from asyncio.windows_events import NULL
import imp
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from .forms import addBidForm, createListingForm, addCommentForm
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.contrib.auth.decorators import login_required


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
    # Check if method of form is post
    if request.method == "POST":

        # Identify the seller of the new listing
        seller = User.objects.get(username = request.user)

        # Capture the data of the new listing from the UI using the form created on forms.py
        form = createListingForm(request.POST)
        if form.is_valid():
            # Save temporarly the data of the form and appending the data with the seller
            listing = form.save(commit=False)
            listing.seller = seller
            # Saving data of new listing in the DB
            listing.save()

            return HttpResponseRedirect(reverse("index"))
        
        else:
            return render(request, "auctions/create.html", {
                'form' : form
                })
    else:
        return render(request, "auctions/create.html", {
            "form": createListingForm()
        })

def listing(request, title):

    # Get the listing data if the listing exist
    listing = get_object_or_404(Listing, title=title)
    state = listing.state
    bid=int(listing.price)

    # Get all comments linking to the listing
    comments = listing.items.all()
    
    # Request DB to know if user has or not the listing as Watchlist

    watcher = request.user
    if request.user.is_anonymous:
        watchlist = False
    else:
        watchlisted = watcher.watchers.all().filter(watch_listing = listing)
        if not watchlisted:
            watchlist = False
        else :
            watchlist = True

    # Data returned to Listing page
    return render(request, "auctions/listing.html",{
        "title" : title,
        "listing" : listing,
        "comments": comments,
        "watchlist" : watchlist,
        "bid": bid,
        "form" : addBidForm(),
        "comment" : addCommentForm(),
        "state" : state
    })

def add_watchlist(request, title):

    # Identify the person logged as watcher
    watcher = request.user

    # Record the action from the UI to add the listing to watchlist
    if request.method == "POST":
        listing = get_object_or_404(Listing, title=title)

        # Save the desire to add to the watchlist to the DB
        watchlist = Watchlist(watcher = watcher, watch_listing = listing)
        watchlist.save()
        
    # Return the user to the listing page
    return HttpResponseRedirect(reverse("listing", args=(title,)))

def remove_watchlist(request, title):
    
    # Identify the person logged as watcher
    watcher = request.user
        
    # Record the action from the UI to remove the listing to watchlist
    if request.method == "POST":
        listing = get_object_or_404(Listing, title=title)
        Watchlist.objects.filter(watcher=watcher, watch_listing =listing).delete()
    return HttpResponseRedirect(reverse("listing", args=(title,)))

def bid(request, title):

    # Retrieve data from the Front End
    if request.method == "POST":

        form = addBidForm(request.POST)
        if form.is_valid():
            bid = float(form.cleaned_data["bid"])
            
            if bid <= 0:
                return render(request, "auctions/error_handling.html",
                {
                    "code": 400,
                    "message": "Bid must be higher than 0"
                })
            
            try:
                bidder = User.objects.get(username = request.user)
                listing = get_object_or_404(Listing, title=title)
            except Listing.DoesNotExist:
                return render (request, "auctions/error_handling.html",
                {
                    "code": 404,
                    "Message": "Listing doesn't exist"
                })

            if listing.seller == bidder:
                return render(request, "auctions/error_handling.html",{
                    "code": 400, 
                    "message": "Seller can't make a bid"
                })

            highest_bid = Bid.objects.filter(auction=listing).order_by('bid').last()
            print(highest_bid)
            if highest_bid is None or bid > highest_bid.bid :
                new_bid = Bid(auction=listing, bidder=bidder, bid=bid)
                new_bid.save()

                listing.price = bid
                listing.buyer = bidder
                listing.save()
            
                return HttpResponseRedirect(reverse("listing", args=(title,)))
            else:
                return render(request, "auctions/error_handling.html", {
                    "code": 400,
                    "message": "Your bid is too small"
                })
        else:
            return render(request, "auctions/error_handling.html",{
                "code": 400,
                "message": "Form is invalid"
            })
        
    return render(request, "auctions/error_handling.html", {
    "code": 405,
    "message": "Method Not Allowed"
})

def close(request, title):
    if request.method == "POST":
        listing = get_object_or_404(Listing, title=title)

        # Save the change of state to the DB
        listing.state = False
        listing.save()
        
    # Return the user to the listing page
    print(listing.state)
    return HttpResponseRedirect(reverse("listing", args=(title,)))

def comment(request, title):
    if request.method == "POST":
        listing = get_object_or_404(Listing, title = title)
        writer = User.objects.get(username = request.user)

        form = addCommentForm(request.POST)
        if form.is_valid():
            comment = form.cleaned_data["content"]
            print(comment)
            new_comment = Comment(writer=writer, item = listing, content = comment)
            new_comment.save()

    return HttpResponseRedirect(reverse("listing", args=(title,)))

def watchlist(request):
    watcher = request.user
    listings = watcher.watchers.all()
    print(listings)

    return render(request, "auctions/watchlist.html",{
        "listings" : listings
    })
    

