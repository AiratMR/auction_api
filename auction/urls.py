from django.urls import path, re_path
from . import views

urlpatterns = [
    re_path(r'^api/v1/auctions/(?P<pk>[0-9]+)$',  # Url to get auction details
            views.GetAuctions.as_view(),
            name='GetAuction'
            ),
    path('api/v1/auctions/',  # urls list all and create new one
         views.GetCreateAuctions.as_view(),
         name='GetCreateAuction'
         )
]
