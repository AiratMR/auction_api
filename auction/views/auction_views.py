from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from ..models import Auction
from ..serializers import AuctionSerializer, AuctionDetailsSerializer
from ..tasks import send_auction_created_message, send_auction_closed_message


class GetAuction(RetrieveAPIView):
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
        Get action details by id.
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
        Get all auctions.

        Query parameters:
            ?status=open | ?status=closed
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
        Create new auction.
        """
        serializer = AuctionSerializer(data=request.data)

        if serializer.is_valid():
            auction = serializer.save(creator=request.user)

            # email notifications
            send_auction_created_message(auction=auction)
            send_auction_closed_message(auction=auction)

            return Response(serializer.data, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)