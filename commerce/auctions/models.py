from pydoc import describe
from unittest.util import _MAX_LENGTH
from django.contrib.auth.models import AbstractUser
from django.db import models



class Listing(models.Model):
    title = models.CharField(max_length=64)
    description = models.TextField()
    starting_bid = models.IntegerField()
    current_price = models.DecimalField(max_digits=100, decimal_places=2)
    url = models.URLField(blank=True) #optionally add url field
    category = models.CharField(blank = True) #optionally add category field
    active = models.BooleanField(default = True) #if the listing is active, default active

class User(AbstractUser):
    watch_list = models.ManyToManyField(Listing, blank = True, related_name = "list_items")

class Bid(models.Model):
    bid = models.DecimalField(max_digits=100, decimal_places=2)

class Comment(models.Model):
    pass