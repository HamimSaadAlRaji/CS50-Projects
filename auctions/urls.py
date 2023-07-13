from django.urls import path

from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("login", views.login_view, name="login"),
    path("logout", views.logout_view, name="logout"),
    path("register", views.register, name="register"),
    path("CreateListing", views.CreateListing, name="CreateListing"),
    path("filter", views.filter, name="filter"),
    path("listing/<int:id>", views.listing, name="listing"),
    path("AddWatchlist/<int:id>", views.AddWatchlist, name="AddWatchlist"),
    path("RemoveWatchlist/<int:id>", views.RemoveWatchlist, name="RemoveWatchlist"),
    path("Watchlist", views.Watchlist, name="Watchlist"),
    path("AddComment/<int:id>", views.AddComment, name="AddComment"),
    path("AddBid/<int:id>", views.AddBid, name="AddBid"),
    path("close/<int:id>", views.close, name="close"),
]
