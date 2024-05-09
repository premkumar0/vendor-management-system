from django.db import models, transaction
from django.db.models.signals import post_save
from django.dispatch import receiver

from vendors.models import HistoricalPerformance, PurchaseOrder


@receiver(post_save, sender=PurchaseOrder)
def update_vendor_metrics(sender, instance, **kwargs):
    if instance.status == "completed":
        vendor = instance.vendor

        # Update on-time delivery rate
        completed_pos = sender.objects.filter(vendor=vendor, status="completed")
        on_time_count = completed_pos.filter(
            delivery_date__gte=models.F("issue_date")
        ).count()
        vendor.on_time_delivery_rate = (
            on_time_count / completed_pos.count() if completed_pos.count() > 0 else 0
        ) * 100

        # Update quality rating average
        vendor.quality_rating_avg = (
            completed_pos.aggregate(models.Avg("quality_rating"))["quality_rating__avg"]
            or 0
        )

        # Update average response time
        total_response_time = sum(
            (po.acknowledgment_date - po.issue_date).total_seconds()
            for po in completed_pos.filter(
                acknowledgment_date__isnull=False, issue_date__isnull=False
            )
        )
        count = completed_pos.filter(
            acknowledgment_date__isnull=False, issue_date__isnull=False
        ).count()

        vendor.average_response_time = total_response_time / count if count > 0 else 0

        # Update fulfillment rate
        total_orders = sender.objects.filter(vendor=vendor)
        vendor.fulfillment_rate = (
            completed_pos.count() / total_orders.count()
            if completed_pos.count() > 0
            else 0
        ) * 100

        with transaction.atomic():
            vendor.save()
            HistoricalPerformance.objects.filter(vendor=vendor).update(
                on_time_delivery_rate=vendor.on_time_delivery_rate,
                quality_rating_avg=vendor.quality_rating_avg,
                average_response_time=vendor.average_response_time,
                fulfillment_rate=vendor.fulfillment_rate,
            )
