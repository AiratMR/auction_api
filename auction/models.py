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

    @staticmethod
    def close_action(pk):
        """
        Close auction
        :param pk: auction primary key (id)
        :return: None
        """
        auction = Auction.objects.filter(pk=pk)
        auction.is_closed = True
        auction.update()


class AuctionBid(models.Model):
    """
    Auction rate

    Attributes:
        user (User): bid creator
        auction (Auction): auction
    """
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    auction = models.ForeignKey(Auction, related_name="bids", on_delete=models.CASCADE)
    price = models.FloatField()
    creation_date = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_last_bid(pk):
        """
        Get last auction bid
        :param pk: auction primary key (id)
        :return: AuctionBid object
        """
        return AuctionBid.objects.filter(auction=pk).latest('creation_date')

    @staticmethod
    def get_auction_users_emails(pk):
        """
        Get users of the auction participants
        :param pk: auction primary key (id)
        :return: List of users
        """

        auction_bids = AuctionBid.objects.filter(auction=pk)

        emails = {auction_bid.user.email for auction_bid in auction_bids}
        return list(emails)
