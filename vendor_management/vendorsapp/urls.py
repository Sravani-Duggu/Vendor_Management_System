# vendorsapp/urls.py
from django.urls import path
from .views import VendorViewSet, PurchaseOrderViewSet, HistoricalPerformanceViewSet

app_name = 'vendorsapp'

urlpatterns = [
    path('vendors/', VendorViewSet.as_view({'get': 'list'}), name='vendor-list'),
    path('purchase_orders/', PurchaseOrderViewSet.as_view({'get': 'list'}), name='purchaseorder-list'),
    path('historical_performance/', HistoricalPerformanceViewSet.as_view({'get': 'list'}), name='historicalperformance-list'),
]


