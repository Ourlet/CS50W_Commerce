from email.mime import image
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils import timezone


class User(AbstractUser):
    pass

class Listing(models.Model):
    title = models.CharField(max_length=32)
    description = models.TextField()
    price = models.IntegerField()
    image = models.URLField(max_length=200, blank=True)
    category = models.CharField(max_length=32)
    creation_date = models.DateField(auto_now=False, auto_now_add=True)
    state = models.BooleanField(default=True)
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name="sellers")
    buyer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="buyer", blank=True)
    watcher = models.ManyToManyField(User, blank=True, related_name="watchers")

    def __str__(self):
        return f"{self.id} : {self.title} by {self.creator}"

class Bid(models.Model):
    auction = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="auction")
    bidder = models.ForeignKey(User, on_delete=models.CASCADE, related_name="bidder")
    bid = models.IntegerField()
    bid_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.auction} by {self.bidder} for {self.bid}"

class Comment(models.Model):
    writer = models.ForeignKey(User, on_delete=models.CASCADE, related_name="writer")
    item = models.ForeignKey(Listing, on_delete=models.CASCADE, related_name="item")
    content = models.TextField()
    comment_creation_date = models.DateField(auto_now=False, auto_now_add=True)

    def __str__(self):
        return f"{self.id} : {self.item} by {self.writer} with {self.content}"