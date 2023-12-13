# vendorsapp/models.py
from django.db import models
from django.utils import timezone

class Vendor(models.Model):
    name = models.CharField(max_length=255)
    contact_details = models.TextField()
    address = models.TextField()
    vendor_code = models.CharField(max_length=50, unique=True)
    on_time_delivery_rate = models.FloatField(default=0.0)
    quality_rating_avg = models.FloatField(default=0.0)
    average_response_time = models.FloatField(default=0.0)
    fulfillment_rate = models.FloatField(default=0.0)

    def __str__(self):
        return self.name

class PurchaseOrder(models.Model):
    po_number = models.CharField(max_length=50, unique=True)
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    order_date = models.DateTimeField()
    delivery_date = models.DateTimeField()
    items = models.JSONField()
    quantity = models.IntegerField()
    status = models.CharField(max_length=50)
    quality_rating = models.FloatField(null=True, blank=True)
    issue_date = models.DateTimeField()
    acknowledgment_date = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"PO {self.po_number} - {self.vendor.name}"

    def save(self, *args, **kwargs):
        is_new = not self.pk
        super().save(*args, **kwargs)

        if is_new or self.status_changed():
            self.vendor.calculate_performance_metrics()

    def status_changed(self):
        try:
            old_status = PurchaseOrder.objects.get(pk=self.pk).status
            return self.status != old_status
        except PurchaseOrder.DoesNotExist:
            return False

    def acknowledge(self):
        self.acknowledgment_date = timezone.now()
        self.save()

    def fulfilled_successfully(self):
        return self.status == 'completed' and self.issue_date <= timezone.now()

    def calculate_on_time_delivery_rate(self):
        completed_orders = self.vendor.purchaseorder_set.filter(status='completed')
        on_time_delivery_orders = completed_orders.filter(delivery_date__lte=timezone.now())
        total_completed_orders = completed_orders.count()
        return (on_time_delivery_orders.count() / total_completed_orders) * 100 if total_completed_orders > 0 else 0.0

    def calculate_quality_rating_avg(self):
        completed_orders = self.vendor.purchaseorder_set.filter(status='completed').exclude(quality_rating=None)
        return completed_orders.aggregate(models.Avg('quality_rating'))['quality_rating__avg'] or 0.0

    def calculate_average_response_time(self):
        acknowledged_orders = self.vendor.purchaseorder_set.filter(status='completed', acknowledgment_date__isnull=False)
        response_times = [po.acknowledgment_date - po.issue_date for po in acknowledged_orders]
        return sum(response_times, models.Duration()) / len(response_times) if len(response_times) > 0 else models.Duration()

    def calculate_fulfillment_rate(self):
        issued_orders = self.vendor.purchaseorder_set.all()
        successful_orders = issued_orders.filter(status='completed', issue_date__lte=timezone.now())
        total_orders = issued_orders.count()
        return (successful_orders.count() / total_orders) * 100 if total_orders > 0 else 0.0

class HistoricalPerformance(models.Model):
    vendor = models.ForeignKey('Vendor', on_delete=models.CASCADE)
    date = models.DateTimeField()
    on_time_delivery_rate = models.FloatField()
    quality_rating_avg = models.FloatField()
    average_response_time = models.FloatField()
    fulfillment_rate = models.FloatField()

    def __str__(self):
        return f"Historical Performance for {self.vendor.name} on {self.date}"



