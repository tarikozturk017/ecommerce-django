from pydoc import describe
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models

from .models import *

class Comment(models.Model):
    comment_title = models.CharField(max_length=64)
    content = models.CharField(max_length = 256)

class Bid(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2)


class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    current_price = models.DecimalField(max_digits=100, decimal_places=2)
    url = models.URLField(blank=True) #optionally add url field
    category = models.CharField(blank = True) #optionally add category field
    active = models.BooleanField(default = True) #if the listing is active, default active
    comments = models.ManyToManyField(Comment, blank = True, related_name="listings")
    bids = models.ManyToManyField(Bid, related_name="listings")

class User(AbstractUser):
    watch_list = models.ManyToManyField(Listing, blank = True, related_name = "user")
    bids = models.ManyToManyField(Bid, blank=True, related_name="user")
    comments = models.ManyToManyField(Comment, blank=True, related_name="user")
