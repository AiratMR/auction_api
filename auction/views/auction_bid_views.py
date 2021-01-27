from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Auction, AuctionBid
from ..serializers import AuctionBidSerializer
from ..permissions import IsOpenAuction, IsNotAuctionOwner
from ..validators import AuctionBidValidator
from ..tasks import send_new_auction_bid_message


class CreateAuctionBid(CreateAPIView):
    serializer_class = AuctionBidSerializer
    permission_classes = (IsAuthenticated, IsOpenAuction, IsNotAuctionOwner,)

    def get_queryset(self, auction_pk):
        try:
            auction_bid = AuctionBid.get_last_bid(auction_pk)
        except AuctionBid.DoesNotExist:
            return None

        return auction_bid

    def post(self, request):
        """
        Create new bid.
        """
        auction_id = int(request.data.get("auction"))
        new_price = float(request.data.get("price"))

        auction = Auction.objects.get(pk=auction_id)
        last_bid = self.get_queryset(auction_id)

        serializer = AuctionBidSerializer(data=request.data)
        if serializer.is_valid():
            if last_bid is None and AuctionBidValidator.is_valid_price(auction.starting_price,
                                                                       new_price,
                                                                       auction.price_step):
                serializer.save(user=request.user)
                # email notification
                send_new_auction_bid_message(auction)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif AuctionBidValidator.is_valid_price(last_bid.price,
                                                    new_price,
                                                    auction.price_step):
                serializer.save(user=request.user)
                # email notification
                send_new_auction_bid_message(auction)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
