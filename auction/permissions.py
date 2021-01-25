from rest_framework import permissions
from .models import Auction


class IsOpenAuction(permissions.BasePermission):
    """
    Object-level permission to only bid on an open auction.
    Assumes the model instance has an `is_closed` attribute.
    """

    def has_permission(self, request, view):
        auction = Auction.objects.get(pk=request.data.get("auction"))
        return not auction.is_closed


class IsNotAuctionOwner(permissions.BasePermission):
    """
    Object-level permission: auction owners can't create bid.
    Assumes the model instance has an `creator` attribute.
    """
    def has_permission(self, request, view):
        auction = Auction.objects.get(pk=request.data.get("auction"))
        return auction.creator.id != request.user.id
