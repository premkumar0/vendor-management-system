"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import include, path

from vendors import views as vend_views

urlpatterns = [
    path("api/token-auth/", vend_views.ObtainToken.as_view()),
    path("api-auth/", include("rest_framework.urls", namespace="rest_framework")),
    # path("admin/", admin.site.urls),
    path("api/vendors/", vend_views.vendors_view, name="vendors"),
    path(
        "api/vendors/<int:vendor_id>/", vend_views.vendor_detail, name="vendor-detail"
    ),
    path(
        "api/vendors/<int:vendor_id>/performance/",
        vend_views.vendor_performance,
        name="vendor-performance",
    ),
    path(
        "api/purchase_orders/", vend_views.purchace_orders_view, name="purchase-orders"
    ),
    path(
        "api/purchase_orders/<int:po_id>/",
        vend_views.purchace_order_detail,
        name="purchase-order-detail",
    ),
]
