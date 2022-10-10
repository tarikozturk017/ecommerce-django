from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.forms import ModelForm
from django.contrib import messages

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

def index(request):
    active_listings = Listing.objects.filter(active=True)
    return render(request, "auctions/index.html", {
        "active_listings": active_listings
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

@login_required
def create_listing(request):
    if request.method == "POST":
        user=request.user
        new_listing = Listing(title=request.POST["title"], description=request.POST["description"], starting_bid=float(request.POST["starting_bid"]), current_price=float(request.POST["starting_bid"]), image_url=request.POST["image_url"], category=request.POST["category"], seller=user)
        new_listing.save()
        return render(request, "auctions/listing.html", {
            "listing": new_listing
        })
    else:
        return render(request, "auctions/create_listing.html", {
            "form": NewListingForm()
        })

@login_required
def listing(request, title):
    user=request.user
    listing = Listing.objects.get(title=title)
    watch_list_check = WatchList.objects.filter(user=user, listing=listing)
    is_exist = True
    if not watch_list_check:
        is_exist = False        
    if request.method == "POST":
        if request.POST["watch_list"] == "add":
            watch_list = WatchList(user=user, listing=listing)
            watch_list.save()
            is_exist = True
        elif request.POST["watch_list"] == "remove":
            watch_list_check.delete()
            is_exist = False
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_exist": is_exist
        })
    else:
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "is_exist": is_exist
        })

@login_required
def bid(request, title):
    if request.method == "POST":
        listing = Listing.objects.get(title=title)
        user=request.user
        bid_amount = float(request.POST["bid_amount"])
        if bid_amount >= listing.current_price:
            new_bid = Bid(amount=bid_amount, bidder=user, listing=listing)
            listing.current_price = new_bid.amount
            listing.save()
            new_bid.save()
        else:
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "message": "Your bid is not bigger than the current bid!"
        })
        bids = Bid.objects.filter(listing=listing)
        return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user,
            "bids": bids
        })