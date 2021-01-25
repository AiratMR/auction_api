from django.db import models
from django.conf import settings


class Auction(models.Model):
    """
    Auction model

    Attributes:
        creator (User): auction creator
        name (str): goods name
        description (str): goods description
        starting_price (float): price at which trading starts
        price_step (float): minimum price step to increase the bid
        creation_date (datetime): auction creation time
        expiration_date (datetime): auction expiration time
        is_closed (bool): auction is closed
        bids (list): auction bids
    """
    creator = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    description = models.TextField()
    starting_price = models.FloatField()
    price_step = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
    expiration_date = models.DateTimeField()
    is_closed = models.BooleanField(default=False)


class AuctionBid(models.Model):
    """
    Auction rate

    Attributes:
        user (User): bid creator
        auction (Auction): auction
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, on_delete=models.CASCADE)
    price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)
