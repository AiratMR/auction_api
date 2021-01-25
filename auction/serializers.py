from django.contrib.auth.models import User
from rest_framework import serializers

from .models import Auction, AuctionBid


class UserSerializer(serializers.ModelSerializer):
    """
    Serializer for User model
    """

    class Meta:
        model = User
        fields = ("id", "username", "email")


class AuctionBidSerializer(serializers.ModelSerializer):
    """
    Serializer for AuctionBid model
    """

    class Meta:
        model = AuctionBid
        fields = ("user", "auction", "price", "creation_date")


class AuctionSerializer(serializers.ModelSerializer):
    """
    Serializer for Auction model
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    expiration_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    class Meta:
        model = Auction
        fields = ("id", "creator", "name", "description", "starting_price",
                  "price_step", "expiration_date", "is_closed")


class AuctionDetailsSerializer(serializers.ModelSerializer):
    """
    Serializer for representing Auction details
    """
    creator = serializers.ReadOnlyField(source='creator.username')
    expiration_date = serializers.DateTimeField(format="%Y-%m-%dT%H:%M:%S")

    bids = AuctionBidSerializer(many=True, read_only=True)

    class Meta:
        model = Auction
        fields = ("id", "creator", "name", "description", "starting_price",
                  "price_step", "expiration_date", "is_closed", "bids")
