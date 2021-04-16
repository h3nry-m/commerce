from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone


class User(AbstractUser):
    test = []


class Listing(models.Model):
    """Creates a Listing class that is connected with the User class"""
    title = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_hx")
    url = models.CharField(max_length=200, default="None")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    """Creates a Bid class that is connected with the User class and Listing class"""
    bid_amount = models.DecimalField(decimal_places=2, max_digits=100)
    timefield = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_hx")
    listing = models.ManyToManyField(
        Listing, related_name="all_bids")

    def __str__(self):
        return f"{self.bid_amount}"


class Comment(models.Model):
    """Creates a comment class that is connected with the User class and Listing class"""
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_hx")
    listing = models.ManyToManyField(
        Listing, related_name="all_comments")

    def __str__(self):
        return f"{self.comment[:50]}"
