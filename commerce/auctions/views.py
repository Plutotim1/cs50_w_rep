from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse
from django.forms import ModelForm
from django.contrib.auth.decorators import login_required

from .models import *


def index(request):
    return render(request, "auctions/index.html", {'listings':Auction.objects.filter()})


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


@login_required(login_url="/login")
def addauction(request):
    class Addauctionform(ModelForm):
        class Meta:
            model = Auction
            fields = ["title", "image_href", "category", "description", "starting_bid", ]
    if request.method == "GET":
        return render(request, "auctions/addauction.html",{"user": request.user,"form": Addauctionform()})
    elif request.method == "POST":
        if Addauctionform(request).is_valid:
            new_auction = Auction(creator=request.user,
            title=request.POST["title"],
            category=request.POST["category"],
            description=request.POST["description"],
            image_href=request.POST["image_href"],
            starting_bid=request.POST["starting_bid"],
            current_price=0)
            new_auction.save()
            return HttpResponseRedirect("/")


def show_listing(request, id):
    if (object := Auction.objects.filter(auction_id=id)[0]):
        return render(request, "auctions/show_auction.html", {"listing": object, "comments": comments.objects.filter(auction=object)})
    else:
        return render(request, "auctions/error.html",{"error_message": "<h4>Listing wasn't found</h4> To check if it was deleted, refresh the starting page to see all currently active listings"})


def add_comment(request):
    #checks if all values aren't null
    if (contents := request.POST["content"]) and (auction_comment_belongs_to := request.POST["auction"]):
        comments(auction=Auction.objects.filter(auction_id=auction_comment_belongs_to)[0],
        content=contents,
        User=request.user).save()
    return HttpResponseRedirect(f"/listing/{auction_comment_belongs_to}")

@login_required(login_url="/login") 
def bid(request):
    bid_value = float(request.POST["bid_value"])
    auctions_id = request.POST["auction_id"]
    if not (auction_bid_on := Auction.objects.filter(auction_id=auctions_id)[0]):
        return error(request, "You entered invalid values!")
    if bid_value >= auction_bid_on.starting_bid and bid_value > auction_bid_on.current_price:
        auction_bid_on.current_price = bid_value
        auction_bid_on.winner = request.user
        auction_bid_on.save(update_fields=["current_price", "winner"])
        new_bid = Bids(
            auction= auction_bid_on,
            amount= bid_value,
            User= request.user
        )
        new_bid.save()
    else:
        return show_error(request,"<p>The current price of the auction is higher than your bid<p>refresh the listing page to see the current price!")
    return HttpResponseRedirect(f"/listing/{auctions_id}")


@login_required(login_url="/login")
def add_to_watchlist(request):
    user = request.user
    if Auction.objects.filter(auction_id=request.POST["auction_id"]):
        user.watchlist.add(request.POST["auction_id"])
    return HttpResponseRedirect(reverse(watchlist))

@login_required(login_url="/login")
def watchlist(request):
    return render(request, "auctions/index.html", {'listings':request.user.watchlist.all})


def show_sort_template(request):
    return render(request, "auctions/sort.html", {"categorys": ["tech", "fashion", "toy", "furniture", "livestyle"]})


def sort(request, category):
    return render(request, "auctions/index.html", {'listings':Auction.objects.filter(category=category)})


def show_error(request, message):
    return render(request, "auctions/error.html", {"error_message": message})


def close_auction(request):
    if not(auction_to_close := Auction.objects.filter(auction_id=request.POST["auction_id"])[0]):
        return show_error(request, "invalid Auction")
    if request.user == auction_to_close.creator:
        auction_to_close.closed = True
        auction_to_close.save(update_fields=["closed"])
    return HttpResponseRedirect(f"/listing/{auction_to_close.auction_id}")

