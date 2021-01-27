from django.urls import path, re_path
from auction.views.auction_views import GetAuction, GetCreateAuctions
from auction.views.auction_bid_views import CreateAuctionBid

urlpatterns = [
    re_path(r'^api/v1/auctions/(?P<pk>[0-9]+)$',  # Url to get auction details
            GetAuction.as_view(),
            name='GetAuction'
            ),
    path('api/v1/auctions/',  # urls list all and create new one
         GetCreateAuctions.as_view(),
         name='GetCreateAuction'
         ),
    path('api/v1/auctionBids/',
         CreateAuctionBid.as_view(),
         name='CreateAuctionBid'
         ),
]
