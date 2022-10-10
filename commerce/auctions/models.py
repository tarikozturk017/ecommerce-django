from pydoc import describe
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

# from .models import *
CATEGORIES = (
    ('Clothing', 'Clothing'),
    ('Furniture', 'Furniture'),
    ('Electronics', 'Electronics'),
    ('Miscellaneous', 'Miscellaneous'),
    ('Kitchen', 'Kitchen'),
    ('None', 'None'),
)

class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.CharField(max_length = 256)
    starting_bid = models.DecimalField(max_digits=20, decimal_places=2)
    current_price = models.DecimalField(max_digits=20, decimal_places=2)
    image_url = models.URLField(null=True, blank=True) #optionally add url field
    category = models.CharField(max_length=64, choices=CATEGORIES, default=CATEGORIES[5][1])
    active = models.BooleanField(default = True) #if the listing is active, default active
    seller = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="listing_sold")
    # buyer = models.ForeignKey(User, null=True, on_delete=models.CASCADE, related_name="listing_bought")

    # def __str__(self):
    #     return f"{self.title}"

class Comment(models.Model):
    comment = models.CharField(max_length = 256)
    listing = models.ForeignKey(Listing, null=False, on_delete=models.CASCADE, related_name="comment")
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="comments")

class Bid(models.Model):
    amount = models.DecimalField(max_digits=20, decimal_places=2)
    bidder = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="bids")
    listing = models.ForeignKey(Listing, null=False, on_delete=models.CASCADE, related_name="bids")

# watch list has 1 user (FK), listings -> many to many relation with Listing 
class WatchList(models.Model):
    user = models.ForeignKey(User, null=False, on_delete=models.CASCADE, related_name="watch_list")
    listing = models.ForeignKey(Listing, on_delete=models.CASCADE, null=True, related_name="listings")

