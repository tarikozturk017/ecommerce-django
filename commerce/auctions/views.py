from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.contrib.auth.decorators import login_required
from .models import *
from django.forms import ModelForm

from django.core.paginator import Paginator


links = [
    "https://im.uniqlo.com/global-cms/spa/res85672dd9b517804065e75b2ae4301a47fr.jpg", 
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRceZuMYxbPGBYiO6jyAkbh21cGr1KFlvJnTQ&usqp=CAU", 
    "https://www.americanchemistry.com/var/site/storage/images/4/8/0/7/7084-2-eng-US/Products-Technology.png",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcSfSGoQJW-dZPCyzXJThBlxeAP59NyAGCjaFMm75DfaQJY1aun75oKLH95fWGnIbHdC-dU&usqp=CAU",
    "https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRUoSApjpqn9Lb7LGKhhC2O2pR2e8bNVrBfiA&usqp=CAU",
    "https://media.istockphoto.com/id/175005911/photo/balls-isolated-on-white.jpg?b=1&s=170667a&w=0&k=20&c=2rV297wFgSPu8Crvc_wQI_dCWJQxrW-QbEi8wep6Wgo=", 
    "https://s3-prod.autonews.com/s3fs-public/styles/width_792/public/6CX30-MAIN.jpg", 
    "https://www.richmondartgallery.org/wp-content/uploads/WE-ASPIRE-650x451.jpg", 
    "https://learn.marsdd.com/wp-content/uploads/2013/12/industry-competition-and-threat_20190730.png"
    ] 

class NewListingForm(ModelForm):
    class Meta:
        model = Listing
        fields = ['title', 'description', 'starting_bid', 'image_url', 'category']

# images = "https://im.uniqlo.com/global-cms/spa/res85672dd9b517804065e75b2ae4301a47fr.jpg"
def index(request):
    active_listings = Listing.objects.filter(active=True)

    #pagination setup
    p = Paginator(Listing.objects.filter(active=True), 6)
    page = request.GET.get('page')
    act_listings_list = p.get_page(page)

    return render(request, "auctions/index.html", {
        "active_listings": active_listings,
        "act_listings_list": act_listings_list
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
        if(new_listing.image_url == ""):
            new_listing.image_url = "https://www.freeiconspng.com/thumbs/no-image-icon/no-image-icon-4.png"
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
            "categories": CATEGORIES,
            "links": links
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
        # listing = None
        # if Listing.objects.filter(title=search_title).count() != 0:
        #     listing = Listing.objects.get(title=search_title)
        # if listing is not None:
        #     return render(request, "auctions/listing.html", {
        #     "listing": listing
        # })
        # else:
        listings = Listing.objects.all()
        foundTitles = []
        for listing in listings:
            # print(f"\n\nTitle: {listing.title}\n\n")
            if listing.title.lower().find(search_title.lower()) != -1:
                foundTitles.append(listing)
        return render(request, "auctions/search.html", {
            "searches": foundTitles
        })
            