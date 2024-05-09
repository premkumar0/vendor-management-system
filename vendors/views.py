from django.contrib.auth.forms import AuthenticationForm
from django.db import transaction
from rest_framework import renderers, status
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.decorators import api_view
from rest_framework.response import Response

from vendors.models import HistoricalPerformance, PurchaseOrder, Vendor
from vendors.serializers import PurchaseOrderSerializer, VendorSerializer


class ObtainToken(ObtainAuthToken):
    form_class = AuthenticationForm
    template_name = "registration/login.html"
    renderer_classes = (renderers.JSONRenderer, renderers.BrowsableAPIRenderer)

    def get(self, request):
        return Response("Please Enter Credentials")


@api_view(["GET", "POST"])
def vendors_view(request):
    """
    List all Vendors and Creates New Vendor
    """
    if request.method == "GET":
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        data = {
            "name": request.data.get("name"),
            "contact_details": request.data.get("contact_details"),
            "address": request.data.get("address"),
        }
        serializer = VendorSerializer(data=data)
        if serializer.is_valid():
            with transaction.atomic():
                vendor = serializer.save()
                hp_obj = HistoricalPerformance.objects.create(vendor=vendor)
                hp_obj.save()
                return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def vendor_detail(request, vendor_id):
    """
    Display, Update, Delete Details of a particular Vendor
    """
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)

    if request.method == "GET":
        serializer = VendorSerializer(vendor)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = {
            "name": request.data.get("name", vendor.name),
            "contact_details": request.data.get(
                "contact_details", vendor.contact_details
            ),
            "address": request.data.get("address", vendor.address),
        }
        serializer = VendorSerializer(vendor, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            print(serializer.data)
            return Response(serializer.data)
        print(serializer.errors)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        vendor.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)


@api_view(["GET"])
def vendor_performance(request, vendor_id):
    try:
        vendor = Vendor.objects.get(pk=vendor_id)
    except Vendor.DoesNotExist:
        return Response({"error": "Vendor not found"}, status=status.HTTP_404_NOT_FOUND)
    context = {
        "name": vendor.name,
        "vendor_code": vendor.vendor_code,
        "on_time_delivery_rate": vendor.on_time_delivery_rate,
        "quality_rating_avg": vendor.quality_rating_avg,
        "average_response_time": vendor.average_response_time,
        "fulfillment_rate": vendor.fulfillment_rate,
    }
    return Response(context)


@api_view(["GET", "POST"])
def purchace_orders_view(request):
    """
    List all Purchase Orders and Creates New Purchase Order
    """
    if request.method == "GET":
        vendor_id = request.query_params.get("filter_by_vendor_id")
        if vendor_id:
            purchase_orders = PurchaseOrder.objects.filter(vendor_id=vendor_id)
        else:
            purchase_orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(purchase_orders, many=True)
        return Response(serializer.data)

    elif request.method == "POST":
        serializer = PurchaseOrderSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(["GET", "PUT", "DELETE"])
def purchace_order_detail(request, po_id):
    """
    Display, Update, Delete Details of a particular Purchase Order
    """
    try:
        purchase_order = PurchaseOrder.objects.get(pk=po_id)
    except PurchaseOrder.DoesNotExist:
        return Response(
            {"error": "Purchase Order not found"}, status=status.HTTP_404_NOT_FOUND
        )

    if request.method == "GET":
        serializer = PurchaseOrderSerializer(purchase_order)
        return Response(serializer.data)

    elif request.method == "PUT":
        data = {
            "order_date": request.data.get("order_date", purchase_order.order_date),
            "delivery_date": request.data.get(
                "delivery_date", purchase_order.delivery_date
            ),
            "items": request.data.get("items", purchase_order.items),
            "quantity": request.data.get("quantity", purchase_order.quantity),
            "status": request.data.get("status", purchase_order.status),
            "quality_rating": request.data.get(
                "quality_rating", purchase_order.quality_rating
            ),
            "issue_date": request.data.get("issue_date", purchase_order.issue_date),
            "acknowledgment_date": request.data.get(
                "acknowledgment_date", purchase_order.acknowledgment_date
            ),
        }

        serializer = PurchaseOrderSerializer(purchase_order, data=data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    elif request.method == "DELETE":
        purchase_order.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
