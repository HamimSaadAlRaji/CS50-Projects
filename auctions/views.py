from django.contrib.auth import authenticate, login, logout
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render
from django.urls import reverse

from .models import User,Category,Listing,Comment,Bid


def index(request):
    CategoryFromForm =Category.objects.all()
    ActiveList = Listing.objects.filter(isActive =True)
    return render(request, "auctions/index.html",{
        "categories":CategoryFromForm,
        "listings":ActiveList
    })


def CreateListing(request):
    if request.method == "GET":
       categorylist =Category.objects.all()
       return render(request, "auctions/CreateListing.html",{
           "categories":categorylist
       })
    
    else:
        title = request.POST["title"]
        description = request.POST["description"]
        image = request.POST["image"]
        price = request.POST["price"]
        owner = request.user
        category = request.POST["category"]
        bid =Bid(bidder=request.user,bid=price)
        bid.save()

        categorytype=Category.objects.get(CategoryName=category)
        newlisting = Listing(
            title =title,
            description =description,
            image =image,
            price =bid,
            owner = owner,
            category =categorytype
        )
        newlisting.save()

        return HttpResponseRedirect(reverse(index))

def filter(request):
    if request.method == "POST":
        CategoryFromForm = request.POST["category"]
        category = Category.objects.get(CategoryName =CategoryFromForm)
        categories =Category.objects.all()
        listing = Listing.objects.filter(isActive =True,category =category)
        return render(request, "auctions/index.html",{
        "categories":categories,
        "listings":listing
    })    

def listing(request,id):    
        item = Listing.objects.get(pk=id)
        IsInWatchlist = request.user in item.watchlist.all()
        comments =Comment.objects.filter(listing=item)
        isOwner = request.user ==item.owner
        
        return render(request,"auctions/listing.html",{
            "listing":item,
            "IsInWatchlist":IsInWatchlist,
            "comments":comments,
            "isOwner":isOwner
        })

def Watchlist(request):
    owner =request.user
    listings = owner.listingwatchlist.all()
    return render(request, "auctions/Watchlist.html",{
         "listings":listings
    })

def RemoveWatchlist(request,id):
        item = Listing.objects.get(pk=id)
        currentuser =request.user
        item.watchlist.remove(currentuser)
        return HttpResponseRedirect(reverse(listing,args=(id, )))

def AddWatchlist(request,id):
        item = Listing.objects.get(pk=id)
        currentuser =request.user
        item.watchlist.add(currentuser)
        return HttpResponseRedirect(reverse(listing,args=(id, )))
def AddComment(request,id):
     item = Listing.objects.get(pk=id)
     owner = request.user
     comment = request.POST["NewComment"]
     newcomment=Comment(
          author =owner,
          comment =comment,
          listing = item

     )
     newcomment.save()
     return HttpResponseRedirect(reverse(listing,args=(id, )))
def AddBid(request,id):
        newbid =request.POST["NewBid"]
        item = Listing.objects.get(pk=id)
        IsInWatchlist = request.user in item.watchlist.all()
        comments =Comment.objects.filter(listing=item)
        isOwner = request.user ==item.owner
        if int(newbid)>item.price.bid:
            updatebid =Bid(bidder =request.user,bid=newbid)
            updatebid.save()
            item.price=updatebid
            item.save() 
            return render(request,"auctions/listing.html",{
            "listing":item,
            "IsInWatchlist":IsInWatchlist,
            "comments":comments,
            "message":"Bid Placed Successfully",
            "isOwner":isOwner,
            "update":True,
            "show":True
            
        })
        else:
            return render(request,"auctions/listing.html",{
            "listing":item,
            "IsInWatchlist":IsInWatchlist,
            "comments":comments,
            "message":"Bid Place Failed",
            "isOwner":isOwner,
            "update":False,
            "show":True
            
        })
def close(request,id):
        item = Listing.objects.get(pk=id)
        IsInWatchlist = request.user in item.watchlist.all()
        comments =Comment.objects.filter(listing=item)
        isOwner = request.user ==item.owner
        item.isActive=False
        item.save()
        winner = item.price.bidder
        
        
        return render(request,"auctions/listing.html",{
            "listing":item,
            "IsInWatchlist":IsInWatchlist,
            "comments":comments,
            "isOwner":isOwner,
            "update":True,
            "show":True,
            "winner":winner
            
            
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
