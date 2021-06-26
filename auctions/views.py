from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from . import forms
from .forms import MakeBid, CommentForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages

from .models import User, Auction, Bid, Comment, Watchlist, Category


def index(request):
    user_id = request.user
    lists = Auction.objects.filter(status="active")
    # if statment because of error 'AnonymousUser' showing
    if user_id.is_authenticated:
        count = Watchlist.objects.filter(user_id=user_id).count()
        return render(request, "auctions/index.html", {
            'lists': lists,
            'count': count
        })
    return render(request, "auctions/index.html", {
        'lists': lists,
    })

def create(request):
    count = Watchlist.objects.filter(user_id=request.user).count()
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
        'count': count
    })

def auction_item(request, item_id):
    user_id = request.user
    item = Auction.objects.get(id=item_id)
    comments = Comment.objects.filter(commment_auctions=item)
    start_bid = Auction.objects.filter(id=item_id).first()
    form = MakeBid()
    comment_form = forms.CommentForm()
    # using actual_bid_price for html page to say which price is acutal from which user
    actual_bid_price = Bid.objects.filter(buyer=user_id, id=item_id)
    # define auction_id=item (for that product (item) actually saying it is (auction_id) from class Watchlist) so after that we can use in html to define function for remove or add to wathclist, as 'if whatchlistt:"
    watchlistt = Watchlist.objects.filter(user_id=user_id, auction_id=item)
    try:
        buyer = Bid.objects.filter(id=item_id).first().buyer
    except:
        buyer = None

    try:
        bid = Bid.objects.filter(id=item_id).first().bid_value
    except:
        bid = 0

    count = Watchlist.objects.filter(user_id=user_id).count()

    return render(request, 'auctions/item.html', {
        'item': item,
        'count': count,
        'form': form,
        'bid_number': bid,
        'start_bid': start_bid,
        'buyer': buyer,
        'comment_form': comment_form,
        'comments': comments,
        'watchlistt': watchlistt,
        'bid': bid,
        'actual_bid_price': actual_bid_price
    })

@login_required
def watchlist(request):
    user_id = request.user
    # user_watchlist - to control Whatchlist of the user who is logged in
    user_watchlist = Watchlist.objects.filter(user_id=user_id)
    count = Watchlist.objects.filter(user_id=user_id).count()
    return render(request, "auctions/watchlist.html", {
        'lists': user_watchlist,
        'count': count
    })

@login_required
def add_to_watchlist(request, item_id):
    user_id = request.user
    item = Auction.objects.get(id=item_id)
    watch_list = Watchlist.objects.filter(user_id=user_id, auction_id=item)
    if watch_list:
        watch_list.delete()
        messages.info(request, 'You have been deleted this product from Watchlist')
        return HttpResponseRedirect(reverse('watchlist'))
    else:
        add = Watchlist(user_id=user_id, auction_id=item)
        add.save()
        messages.info(request, 'You have been added this product to Watchlist')
        return HttpResponseRedirect(reverse('watchlist'))


@login_required
def make_bid(request, item_id):
    user_id = request.user
    item = Auction.objects.get(id=item_id)
    start_bid = Auction.objects.filter(id=item_id).first()
    try:
        bid = Bid.objects.filter(id=item_id).first().bid_value
    except:
        bid = 0
    if request.method == 'POST':
        form = MakeBid(request.POST)
        if form.is_valid():
            bid_value = form.cleaned_data['bid_value']
            if bid_value > start_bid.start_bit and bid_value > bid:
                instance = form.save(commit=False)
                instance.buyer = user_id
                instance.id = item_id
                instance.save()
                return HttpResponseRedirect(reverse('item', args=(item.id,)))
            else:
                messages.error(request, "Your bid is invalid or smaller than actual prise/bid")
                return HttpResponseRedirect(reverse('item', args=(item.id,)))

    return render(request, "auctions/item.html", {
        'form': form
            })

@login_required
def close_bid(request, item_id):
    item = Auction.objects.get(id=item_id)
    item.status = 'sold'
    item.save()
    return HttpResponseRedirect(reverse('index'))

@login_required
def add_comment(request, item_id):
    user_id = request.user
    item = Auction.objects.get(id=item_id)
    if request.method == 'POST':
        form = forms.CommentForm(request.POST)
        if form.is_valid():
            instance = form.save(commit=False)
            instance.comment_user = user_id
            instance.commment_auctions = item
            instance.save()
            return HttpResponseRedirect(reverse('item', args=(item.id,)))
        else:
            return render(request, "auctions/item.html", {
                'form': form,
            })
    return render(request, "auctions/item.html", {
        'formm': CommentForm(),
        'formmm': Comment(),
        'item': item,
        })


@login_required
def categories(request):
    count = Watchlist.objects.filter(user_id=request.user).count()
    categories = Category.objects.all()
    return render(request, "auctions/categories.html", {
        'categories': categories,
        'count': count
    })

@login_required
def category(request, id):
    count = Watchlist.objects.filter(user_id=request.user).count()
    # to take Category id
    categoryy = Category.objects.get(pk=id)
    # to define that select_category from Auction is = to id from Category
    select_category = Auction.objects.filter(select_category=categoryy)
    return render(request, "auctions/category.html", {
        'select_category': select_category,
        'categoryy': categoryy,
        'count': count
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