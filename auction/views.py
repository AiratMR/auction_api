from datetime import datetime
from rest_framework.permissions import IsAuthenticated
from rest_framework.generics import ListCreateAPIView, RetrieveAPIView
from rest_framework.response import Response
from rest_framework import status

from .models import Auction
from .serializers import AuctionSerializer, AuctionDetailsSerializer


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
        auction = self.get_queryset(pk)
        serialized = AuctionDetailsSerializer(auction)
        return Response(serialized.data, status=status.HTTP_200_OK)


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
        :return: auction list
        """
        auctions = self.get_queryset()
        auction_status = self.request.query_params.get('status', None)

        if auction_status is not None:
            if auction_status == 'open':
                auctions = auctions.filter(is_closed=False)
            elif auction_status == 'closed':
                auctions = auctions.filter(is_closed=True)

        serialized = AuctionSerializer(auctions, many=True)
        return Response({"auctions": serialized.data})

    def post(self, request):
        """
        Create auction
        :param request: request object
        :return: Response
        """
        serialized = AuctionSerializer(data=request.data)

        if serialized.is_valid():
            serialized.save(creator=request.user, creation_date=datetime.utcnow())
            return Response(serialized.data, status=status.HTTP_201_CREATED)

        return Response(serialized.errors, status=status.HTTP_400_BAD_REQUEST)
