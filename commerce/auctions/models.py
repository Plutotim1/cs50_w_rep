from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    watchlist = models.ManyToManyField("Auction", blank=True, related_name="User")


class Auction(models.Model):
    auction_id = models.IntegerField(primary_key=True)
    creator = models.ForeignKey('User', on_delete=models.CASCADE, related_name='auctions')
    winner = models.ForeignKey("User", on_delete=models.SET_NULL, null=True, blank=True, related_name="auctions_won")
    title = models.CharField(max_length=100)
    image_href = models.CharField(max_length=5000, blank=True)
    category = models.CharField(choices=[
        (TECH := 'tech', 'technical'),
        (FASHION := 'fashion', 'fashion'),
        (TOY := 'toy', 'toys'),
        (FURN := 'furniture', 'furniture'),
        (LIVESTYLE := "livestyle", "livestyle")], max_length=16, blank=True)
    description = models.CharField(max_length=256)
    starting_bid = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    current_price = models.DecimalField(max_digits=9, decimal_places=2, default=0.00)
    closed = models.BooleanField(blank=True, default=False)




class Bids(models.Model):
    auction = models.ForeignKey('Auction',on_delete=models.CASCADE, null=True, related_name="bids")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    User = models.ForeignKey('User',on_delete=models.CASCADE, null=True, related_name="bids")


class comments(models.Model):
    auction = models.ForeignKey('Auction', on_delete=models.CASCADE, null=True, related_name="comments")
    content = models.CharField(max_length=1024)
    User = models.ForeignKey('User', on_delete=models.SET_NULL, null=True, related_name="comments")