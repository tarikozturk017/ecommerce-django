from turtle import textinput
from typing import List
from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.forms import ModelForm

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

@login_required(login_url='login')
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

def listing(request, title):
    listing = Listing.objects.get(title=title)
    if request.user.is_authenticated:
        user=request.user
        
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
                "is_exist": is_exist,
                "user": user
            })
        else:
            return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_exist": is_exist
            })
    else:
        return render(request, "auctions/listing.html", {
                "listing": listing,
                "is_not_logged": True
            })

@login_required(login_url='login')
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

@login_required(login_url='login')
def close_bid(request, title):
    if request.method == "POST":
        user=request.user
        if request.POST["close_bid"] == "close":
            listing = Listing.objects.get(title=title)
            buyer = listing.bids.all().last().bidder
            listing.buyer = buyer
            listing.active = False
            listing.save()
            return render(request, "auctions/listing.html", {
            "listing": listing,
            "user": user
        })

@login_required(login_url='login')
def comment(request, title):
    if request.method == "POST":
        comment = request.POST["comment"]
        listing = Listing.objects.get(title=title)
        user=request.user
        new_comment = Comment(comment=comment, listing=listing, user=user)
        new_comment.save()
        return render(request, "auctions/listing.html", {
            "listing": listing
        })

def categories(request):
    if request.method == "GET":
        return render(request, "auctions/categories.html", {
            "categories": CATEGORIES
        })


def category(request, category):
    if request.method == "GET":
        listings = Listing.objects.filter(category=category, active=True)
        return render(request, "auctions/category.html", {
            "listings": listings
        })

@login_required(login_url='login')
def watch_list(request):
    if request.method == "GET":
        user = request.user
        watch_lists = WatchList.objects.filter(user=user)
        return render(request, "auctions/watch_list.html", {
            "watch_lists": watch_lists
        })
        
def search(request):
    if request.method == "POST":
        search_title = request.POST['search'] # looks for name="q" in layout
        listing = None
        if Listing.objects.filter(title=search_title).count() != 0:
            listing = Listing.objects.get(title=search_title)
        if listing is not None:
            return render(request, "auctions/listing.html", {
            "listing": listing
        })
        else:
            listings = Listing.objects.all()
            foundTitles = []
            for listing in listings:
                # print(f"\n\nTitle: {listing.title}\n\n")
                if listing.title.find(search_title) != -1:
                    foundTitles.append(listing.title)

            for found in foundTitles:
                print(f"\n\nFound Title: {found}\n\n")
            return render(request, "auctions/search.html", {
                "searches": foundTitles
            })
            