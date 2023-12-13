# vendorsapp/serializers.py
from rest_framework import serializers
from .models import Vendor, PurchaseOrder, HistoricalPerformance

class HistoricalPerformanceSerializer(serializers.ModelSerializer):
    class Meta:
        model = HistoricalPerformance
        fields = '__all__'

class PurchaseOrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = PurchaseOrder
        fields = '__all__'

class VendorSerializer(serializers.ModelSerializer):
    historicalperformance_set = HistoricalPerformanceSerializer(many=True, read_only=True)
    purchaseorder_set = PurchaseOrderSerializer(many=True, read_only=True)

    class Meta:
        model = Vendor
        fields = '__all__'


