from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from . import forms

from .models import User, Auction, Bid, Comment

# class CreateForm(forms.Form):
#     title = forms.CharField(label='Create title ')

def index(request):
    lists = Auction.objects.all()
    return render(request, "auctions/index.html", {
        'lists':lists
    })

def create(request):
    if request.method == 'POST':
        form = forms.CreateAuction(request.POST, request.FILES)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.seller = request.user
            instance.save()
            return HttpResponseRedirect(reverse("index"))
    else:
        form = forms.CreateAuction()
    return render(request, "auctions/create.html", {
        'form': form,
    })

def auction_item(requset, item_id):
    item = Auction.objects.get(id=item_id)
    return render(requset, 'auctions/item.html', {
        'item': item,
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


