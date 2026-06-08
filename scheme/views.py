from django.shortcuts import render, redirect, get_object_or_404
from nyondo.models import Stock, Sale
from .models import SchemeCustomer, SchemePayment, SchemeGoodsPickup
from django.db.models import Sum
from nyondo.models import Stock
import re
from decimal import Decimal
from django.contrib import messages
from users.decorators import admin_or_sales_manager_required
from django.contrib.auth.decorators import login_required

# Create your views here.

@login_required
@admin_or_sales_manager_required
def scheme_customer_list(request):
    customers = SchemeCustomer.objects.all().order_by("-date_registered")
    return render(request, "scheme_customer_list.html", {"customers": customers})


@login_required
@admin_or_sales_manager_required
def register_scheme_customer(request):
    if request.method == "POST":
        full_name = request.POST.get("full_name", "").strip()
        nin_number = request.POST.get("nin_number", "").strip().upper()
        phone_number = request.POST.get("phone_number", "").strip()
        address = request.POST.get("address", "").strip()
        occupation = request.POST.get("occupation", "").strip()
        employer_name = request.POST.get("employer_name", "").strip()

        errors = {}

        nin_pattern = r"^(CM|CF)[0-9]{10}[A-Z]{2}$"
        phone_pattern = r"^07[0-9]{8}$"

        if not full_name:
            errors["full_name_error"] = "Full name is required."

        if not nin_number:
            errors["nin_error"] = "NIN number is required."
        elif not re.match(nin_pattern, nin_number):
            errors["nin_error"] = "Invalid NIN format. Use format like CM1234567890AB."
        elif SchemeCustomer.objects.filter(nin_number=nin_number).exists():
            errors["nin_error"] = "A customer with this NIN already exists."

        if not phone_number:
            errors["phone_error"] = "Phone number is required."
        elif not re.match(phone_pattern, phone_number):
            errors["phone_error"] = "Invalid phone number. Use format like 0781234567."

        if not address:
            errors["address_error"] = "Address is required."

        if not occupation:
            errors["occupation_error"] = "Occupation is required."

        if errors:
            return render(request, "register_scheme_customer.html", {
                "errors": errors,
                "form_data": request.POST
            })

        SchemeCustomer.objects.create(
            full_name=full_name,
            nin_number=nin_number,
            phone_number=phone_number,
            address=address,
            occupation=occupation,
            employer_name=employer_name
        )

        messages.success(request, "Scheme customer registered successfully.")
        return redirect("scheme_customer_list")

    return render(request, "register_scheme_customer.html", {
        "errors": {},
        "form_data": {}
    })


@login_required
@admin_or_sales_manager_required
def record_scheme_payment(request, customer_id):
    customer = get_object_or_404(SchemeCustomer, id=customer_id)

    if request.method == "POST":
        payment = SchemePayment.objects.create(
            customer=customer,
            amount_paid=request.POST.get("amount_paid"),
            notes=request.POST.get("notes"),
        )

        return redirect("scheme_receipt", payment_id=payment.id)

    return render(request, "record_scheme_payment.html", {"customer": customer})

@login_required
@admin_or_sales_manager_required
def scheme_receipt(request, payment_id):
    payment = get_object_or_404(SchemePayment, id=payment_id)
    return render(request, "scheme_receipt.html", {"payment": payment})


@login_required
@admin_or_sales_manager_required
def customer_scheme_detail(request, customer_id):
    customer = get_object_or_404(SchemeCustomer, id=customer_id)
    payments = SchemePayment.objects.filter(customer=customer)
    pickups = SchemeGoodsPickup.objects.filter(customer=customer)

    total_paid = sum(payment.amount_paid for payment in payments)
    total_goods_value = sum(
        pickup.quantity_taken * pickup.product.unit_price for pickup in pickups
    )

    balance = total_paid - total_goods_value

    return render(request, "customer_scheme_detail.html", {
        "customer": customer,
        "payments": payments,
        "pickups": pickups,
        "total_paid": total_paid,
        "total_goods_value": total_goods_value,
        "balance": balance,
    })


@login_required
@admin_or_sales_manager_required
def scheme_goods_pickup(request, customer_id):
    customer = get_object_or_404(SchemeCustomer, id=customer_id)

    products = Stock.objects.filter(
        category__in=[
            "Cement",
            "Iron Sheets",
            "Iron Bars"
        ]
    )

    if request.method == "POST":

        product = get_object_or_404(
            Stock,
            id=request.POST.get("product")
        )

        quantity = int(request.POST.get("quantity"))

        # TOTAL STOCK RECEIVED
        total_received = Stock.objects.filter(
            product_name=product.product_name
        ).aggregate(
            total=Sum("quantity_delivered")
        )["total"] or 0

        # TOTAL STOCK SOLD
        total_sold = Sale.objects.filter(
            product=product
        ).aggregate(
            total=Sum("quantity")
        )["total"] or 0

        # AVAILABLE STOCK
        available_stock = total_received - total_sold

        # VALIDATE STOCK
        if quantity > available_stock:

            return render(
                request,
                "scheme_goods_pickup.html",
                {
                    "customer": customer,
                    "products": products,
                    "error": (
                        f"Not enough stock available. "
                        f"Current stock is {available_stock}."
                    )
                }
            )

        # CALCULATE TOTAL PRICE
        sub_total = product.unit_price * Decimal(quantity)

        # CREATE SALE RECORD
        sale = Sale.objects.create(
            customer_name=customer.full_name,
            product=product,
            quantity=quantity,
            sub_total=sub_total,
            payment_method="Scheme",
            distance_km=Decimal("0"),
            transport_required=False,
            transport_fee=Decimal("0"),
            total_price=sub_total
        )

        # CREATE GOODS PICKUP RECORD
        SchemeGoodsPickup.objects.create(
            customer=customer,
            product=product,
            quantity_taken=quantity,
            linked_sale=sale
        )

        return redirect(
            "sales_receipt",
            sale_id=sale.id
        )

    return render(
        request,
        "scheme_goods_pickup.html",
        {
            "customer": customer,
            "products": products,
        }
    )