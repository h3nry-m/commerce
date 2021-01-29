from django.contrib.auth.models import AbstractUser
from django.db import models
from datetime import date
from django.utils import timezone


class User(AbstractUser):
    pass


# class Category(models.Model):
#     possible_categories = [
#         ("NONE", "Not applicable"),
#         ("CAR", "Automobile"),
#         ("BOOK", "Book"),
#         ("EXERCISE", "Exercise"),
#         ("FOOD", "Food"),
#         ("HOME", "Home"),
#         ("WORK", "Work"), ]
#     category = models.CharField(
#         max_length=64,
#         choices=possible_categories, default="NONE")


class Listing(models.Model):
    title = models.CharField(max_length=64)
    price = models.DecimalField(decimal_places=2, max_digits=100)
    description = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="listing_hx")
    url = models.CharField(max_length=200, default="None")
    # category = models.ManyToManyField(Category, related_name="listing")

    def __str__(self):
        return f"{self.title}"


class Bid(models.Model):
    bid_amount = models.DecimalField(decimal_places=2, max_digits=100)
    timefield = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="bid_hx")
    listing = models.ManyToManyField(
        Listing, related_name="all_bids")

    def __str__(self):
        return f"{self.bid_amount}"


class Comment(models.Model):
    comment = models.CharField(max_length=200)
    user = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name="comment_hx")
    listing = models.ManyToManyField(
        Listing, related_name="all_comments")

    def __str__(self):
        return f"{self.comment[:50]}"
