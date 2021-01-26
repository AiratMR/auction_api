from config import celery_app
from django.core.mail import send_mail
from django.contrib.auth.models import User

from config.settings import EMAIL_HOST_USER
from .models import AuctionBid, Auction


def send_auction_created_message(auction):
    """
    Send a message about creating an auction to users

    :param auction: Auction object
    :return: None
    """
    send_auction_created_task.apply_async(
        [auction.name,
         auction.description,
         auction.starting_price,
         auction.price_step]
    )


@celery_app.task
def send_auction_created_task(auction_name, description, starting_price, price_step):
    """
    Send a message about creating an auction to users task
    :param auction_name: created auction name
    :param description: auction description
    :param starting_price: auction starting price
    :param price_step: auction price step
    :return: None
    """
    receivers = [user.email for user in User.objects.all()]

    send_mail(
        'New auction',
        str.format("""
            New auction - {0}:
            
            {1}
            Starting price: {2},
            Price step: {3}.
            """, auction_name, description, starting_price, price_step),
        EMAIL_HOST_USER,
        receivers
    )


def send_auction_closed_message(auction):
    """
    Send a message to close the auction

    :param auction: auction object
    :return: None
    """

    expiration_time = auction.expiration_date - auction.creation_date
    countdown = expiration_time.total_seconds()
    send_auction_closed_task.apply_async([auction.pk], countdown=countdown)


@celery_app.task
def send_auction_closed_task(auction_id):
    """
    Send a message to close the auction task

    :param auction_id: auction id
    :return: None
    """
    Auction.close_action(auction_id)

    last_bid = AuctionBid.get_last_bid(auction_id)

    send_mail(
        'Auction closed.',
        str.format("""
            You won auction - {0}:

            Total price: {1}.
            """, last_bid.auction.name, last_bid.price),
        EMAIL_HOST_USER,
        [last_bid.user.email]
    )

    send_mail(
        'Auction closed.',
        str.format("""
           Auction for goods - {0} is closed.
    
           Total price: {1}.
           """, last_bid.auction.name, last_bid.price),
        EMAIL_HOST_USER,
        AuctionBid.get_auction_users_emails(auction_id)
    )


def send_new_auction_bid_message(auction):
    """
    Send a message about a new bid to all auction participants
    :param auction: auction object
    :return: None
    """

    send_new_auction_bid_task.apply_async([auction.pk])


@celery_app.task
def send_new_auction_bid_task(auction_id):
    """
    Send a message about a new bid to all auction participants task
    :param auction_id: auction id
    :return: None
    """
    last_bid = AuctionBid.get_last_bid(auction_id)

    send_mail(
        'New auction bid.',
        str.format("""
           New bid for goods - {0}.

           New price: {1}.
           """, last_bid.auction.name, last_bid.price),
        EMAIL_HOST_USER,
        AuctionBid.get_auction_users_emails(auction_id)
    )
