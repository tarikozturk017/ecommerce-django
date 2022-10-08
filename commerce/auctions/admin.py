from django.contrib import admin
from .models import *

# TO DO -> list displays 

# Register your models here.
admin.site.register(Listing)
admin.site.register(User)
admin.site.register(Bid)
admin.site.register(Comment)