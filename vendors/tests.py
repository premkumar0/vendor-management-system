from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from vendors.models import PurchaseOrder, Vendor
from vendors.serializers import PurchaseOrderSerializer, VendorSerializer
from django.contrib.auth.models import User
from rest_framework.authtoken.models import Token

from django.contrib.auth.models import User


class VendorTests(APITestCase):
    def setUp(self):
        # Create some sample vendors
        self.vendor1 = Vendor.objects.create(
            name="Vendor A", contact_details="+91 123456789", address="India"
        )
        self.vendor2 = Vendor.objects.create(
            name="Vendor B", contact_details="+91 123456789", address="India"
        )
        new_user = User.objects.create_user(
            "test_user", "email@example.com", "Tester@321"
        )
        new_user.first_name = "John"
        new_user.last_name = "Doe"
        new_user.is_staff = True
        new_user.save()
        self.token, created = Token.objects.get_or_create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_list_vendors(self):
        """
        Ensure we can list all vendors.
        """
        url = reverse("vendors")
        response = self.client.get(url)
        vendors = Vendor.objects.all()
        serializer = VendorSerializer(vendors, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_vendor(self):
        """
        Ensure we can create a new vendor.
        """
        url = reverse("vendors")
        data = {
            "name": "Vendor C",
            "contact_details": "+91 123456789",
            "address": "India",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Vendor.objects.count(), 3)
        self.assertEqual(Vendor.objects.get(pk=3).name, "Vendor C")

    def test_get_vendor(self):
        """
        Ensure we can list all vendors.
        """
        url = reverse("vendor-detail", kwargs={"vendor_id": self.vendor1.pk})
        response = self.client.get(url)
        serializer = VendorSerializer(self.vendor1)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_vendor(self):
        """
        Ensure we can update an existing vendor.
        """
        url = reverse("vendor-detail", kwargs={"vendor_id": self.vendor1.pk})
        data = {"name": "Vendor A Updated"}
        response = self.client.put(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(
            Vendor.objects.get(pk=self.vendor1.pk).name, "Vendor A Updated"
        )

    def test_delete_vendor(self):
        """
        Ensure we can delete a vendor.
        """
        url = reverse("vendor-detail", kwargs={"vendor_id": self.vendor1.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Vendor.objects.count(), 1)


class PurchaseOrderTests(APITestCase):
    def setUp(self):
        self.vendor = Vendor.objects.create(
            name="Vendor X", contact_details="+91 123456789", address="India"
        )
        self.po = PurchaseOrder.objects.create(
            vendor=self.vendor,
            order_date="2023-01-01T00:00:00Z",
            delivery_date="2023-01-10T00:00:00Z",
            items="{'item1': '10', 'item2': '20'}",
            quantity=30,
            status="pending",
            quality_rating=4.5,
            issue_date="2023-01-02T00:00:00Z",
            acknowledgment_date="2023-01-03T00:00:00Z",
        )
        new_user = User.objects.create_user(
            "test_user", "email@example.com", "Tester@321"
        )
        new_user.first_name = "John"
        new_user.last_name = "Doe"
        new_user.is_staff = True
        new_user.save()
        self.token, created = Token.objects.get_or_create(user=new_user)
        self.client.credentials(HTTP_AUTHORIZATION="Token " + self.token.key)

    def test_list_purchase_orders(self):
        """
        Ensure we can list all purchase orders.
        """
        url = reverse("purchase-orders")
        response = self.client.get(url)
        orders = PurchaseOrder.objects.all()
        serializer = PurchaseOrderSerializer(orders, many=True)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_create_purchase_order(self):
        """
        Ensure we can create a new purchase order.
        """
        url = reverse("purchase-orders")
        data = {
            "vendor": self.vendor.pk,
            "order_date": "2023-02-01",
            "delivery_date": "2023-02-10",
            "items": "{'item3': '30', 'item4': '40'}",
            "quantity": 70,
            "status": "completed",
            "quality_rating": 3.5,
            "issue_date": "2023-02-02",
            "acknowledgment_date": "2023-02-03",
        }
        response = self.client.post(url, data, format="json")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(PurchaseOrder.objects.count(), 2)

    def test_get_purchase_order(self):
        """
        Ensure we can retrieve a single purchase order.
        """
        url = reverse("purchase-order-detail", kwargs={"po_id": self.po.pk})
        response = self.client.get(url)
        serializer = PurchaseOrderSerializer(self.po)
        self.assertEqual(response.data, serializer.data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_update_purchase_order(self):
        """
        Ensure we can update an existing purchase order.
        """
        url = reverse("purchase-order-detail", kwargs={"po_id": self.po.pk})
        data = {
            "status": "completed",
            "quality_rating": 5.0,
        }
        response = self.client.put(url, data, format="json")
        self.po.refresh_from_db()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(self.po.status, "completed")
        self.assertEqual(self.po.quality_rating, 5.0)

    def test_delete_purchase_order(self):
        """
        Ensure we can delete a purchase order.
        """
        url = reverse("purchase-order-detail", kwargs={"po_id": self.po.pk})
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(PurchaseOrder.objects.count(), 0)
