from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django import forms

from .models import User, Listing, Bid, Comment


class ListingForm(forms.Form):
    """A class for creating new forms"""
    title = forms.CharField(label='Title')
    price = forms.FloatField(label='Price')
    description = forms.CharField(label='Description')
    # url = forms.CharField(label='url')


def index(request):
    """The main page has a list of all listings"""
    return render(request, "auctions/index.html", {
        "Listings": Listing.objects.all(),
    })


def create(request):
    """Creates a new listing"""
    if request.method == "POST":
        form = ListingForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            price = form.cleaned_data['price']
            description = form.cleaned_data['description']
            new = Listing(title=title, price=price,
                          description=description, user=request.user)
            new.save()
            return HttpResponseRedirect(reverse("listing", args=(new.pk,)))
    return render(request, "auctions/create.html", {
        "form": ListingForm(),
    })


def watchlist(request):
    """Adds a listing to the watchlist"""
    if request.method == 'POST':
        listing_number = request.POST['add_watchlist']
        listing_object = Listing.objects.get(pk=listing_number)
        request.user.add(test=listing_object)
        # request.user.test.append(listing_object)
    return render(request, "auctions/watchlist.html", {
        "watchlist": request.user.test,
    })


def categories(request):
    """Renders the category page"""
    return render(request, "auctions/categories.html")


def listing(request, listing_number):
    """Renders the information of the listing. Will allow for posting new comments and bids"""
    listing_detail = Listing.objects.get(pk=listing_number)
    if request.method == 'POST':
        print(request.POST)
        if 'new_comment' in request.POST:
            new_comment = request.POST['new_comment']
            testing = Comment(comment=new_comment, user=request.user)
            testing.save()
            testing.listing.add(listing_detail)
            testing.save()
        elif "new_bid" in request.POST:
            new_bid = request.POST['new_bid']
            testing = Bid(bid_amount=new_bid, user=request.user)
            testing.save()
            testing.listing.add(listing_detail)
            testing.save()
    current_bid = listing_detail.all_bids.all().last()
    return render(request, "auctions/listing.html", {
        "Listing": listing_detail,
        "Comments": listing_detail.all_comments.all(),
        "Current_Bid": current_bid,
    })


def login_view(request):
    """Logs in the user"""
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
    """Logs out the user"""
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
