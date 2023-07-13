from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    pass

class Category(models.Model):
    CategoryName = models.CharField(max_length= 64)
    def __str__(self):
        return self.CategoryName
class Bid(models.Model):
    bidder = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="bidder")
    bid =models.IntegerField()


class Listing(models.Model):    
    title =models.CharField(max_length= 64)
    description = models.CharField(max_length= 500)
    image = models.CharField(max_length= 500)
    price = models.ForeignKey(Bid,on_delete=models.CASCADE,null=True,related_name="price")
    isActive =models.BooleanField(default=True)
    owner = models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="user")
    category = models.ForeignKey(Category,on_delete=models.CASCADE,null=True,blank=True,related_name="category")
    watchlist = models.ManyToManyField(User,null=True,blank=True,related_name="listingwatchlist")
    def __str__(self):
        return self.title
class Comment(models.Model):
    author =  models.ForeignKey(User,on_delete=models.CASCADE,null=True,related_name="usercomment")
    comment = models.CharField(max_length= 200)
    listing = models.ForeignKey(Listing,on_delete=models.CASCADE,null=True,related_name="commentedlist")