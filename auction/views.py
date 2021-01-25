from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView, CreateAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Auction, AuctionBid
from .serializers import AuctionSerializer, AuctionDetailsSerializer, AuctionBidSerializer
from .permissions import IsOpenAuction, IsNotAuctionOwner
from .validators import AuctionBidValidator


class GetAuctions(RetrieveAPIView):
    serializer_class = AuctionDetailsSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self, pk):
        try:
            auction = Auction.objects.get(pk=pk)
        except Auction.DoesNotExist:
            content = {
                'status': 'Not Found'
            }
            return Response(content, status=status.HTTP_404_NOT_FOUND)
        return auction

    def get(self, request, pk):
        """
        Get action details bu id
        :param request: request object
        :param pk: primary key (id)
        :return: serialized Auction object
        """
        auction = self.get_queryset(pk)
        serializer = AuctionDetailsSerializer(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetCreateAuctions(ListCreateAPIView):
    serializer_class = AuctionSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        auctions = Auction.objects.all()
        return auctions

    def get(self, request):
        """
        Get all auctions
        :param request: request object
        :return: Serialized Auction list
        """
        auctions = self.get_queryset()
        auction_status = self.request.query_params.get('status', None)

        if auction_status is not None:
            if auction_status == 'open':
                auctions = auctions.filter(is_closed=False)
            elif auction_status == 'closed':
                auctions = auctions.filter(is_closed=True)

        serializer = AuctionSerializer(auctions, many=True)
        return Response({"auctions": serializer.data})

    def post(self, request):
        """
        Create auction
        :param request: request object
        :return: Response
        """
        serializer = AuctionSerializer(data=request.data)

        if serializer.is_valid():
            serializer.save(creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        # todo: оповещение пользователей об открытом аукционе
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class CreateAuctionBid(CreateAPIView):
    serializer_class = AuctionBidSerializer
    permission_classes = (IsAuthenticated, IsOpenAuction, IsNotAuctionOwner,)

    def get_queryset(self, auction_pk):
        try:
            auction_bid = AuctionBid.objects.filter(auction=auction_pk).latest('creation_date')
        except AuctionBid.DoesNotExist:
            return None

        return auction_bid

    def post(self, request):
        """
        Create new bid
        :param request: request object
        :return: Response
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
                return Response(serializer.data, status=status.HTTP_201_CREATED)

            elif AuctionBidValidator.is_valid_price(last_bid.price,
                                                    new_price,
                                                    auction.price_step):
                serializer.save(user=request.user)
                return Response(serializer.data, status=status.HTTP_201_CREATED)

        # todo: оповещение пользователей об открытом аукционе
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
