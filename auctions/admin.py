from django.contrib import admin

from .models import Auction, Category, Watchlist

# Register your models here.
admin.site.register(Auction)
admin.site.register(Category)
admin.site.register(Watchlist)
