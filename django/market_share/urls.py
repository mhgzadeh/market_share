from django.urls import path
from market_share.views import CalculateMarketShare

urlpatterns = [
    path('', CalculateMarketShare.as_view(), name='market_share__calculate_market_share'),
]
