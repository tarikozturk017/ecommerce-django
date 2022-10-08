from django.contrib import admin
from .models import *

# TO DO -> list displays 

# Register your models here.
admin.site(Listing)
admin.site(User)
admin.site(Bid)
admin.site(Comment)