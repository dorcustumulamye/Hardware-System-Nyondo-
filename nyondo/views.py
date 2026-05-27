from decimal import Decimal
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import authenticate, login
from .models import Sale, Stock
from .models import StockReceipt



# Create your views here.
#Views for stock management
def add_stock(request):

    if request.method == 'POST':

        # Debug: print all submitted form data
        print("===== FORM DATA RECEIVED =====")
        print(request.POST)

        supplier = request.POST.get('supplier')
        category = request.POST.get('category')
        product_name = request.POST.get('product_name')
        quantity_delivered = request.POST.get('quantity_delivered')
        unit_cost = request.POST.get('unit_cost')
        unit_price = request.POST.get('unit_price')
        supplier_payment_status = request.POST.get('supplier_payment_status')
        payment_type = request.POST.get('payment_type')

       
        print(f"Supplier: {supplier}")
        print(f"Category: {category}")
        print(f"Product Name: {product_name}")
        print(f"Quantity Delivered: {quantity_delivered}")
        print(f"Unit Cost: {unit_cost}")
        print(f"Unit Price: {unit_price}")
        print(f"Supplier Payment Status: {supplier_payment_status}")
        print(f"Payment Type: {payment_type}")

        try:
            stock = Stock.objects.create(
                supplier=supplier,
                category=category,
                product_name=product_name,
                quantity_delivered=int(quantity_delivered),
                unit_cost=Decimal(unit_cost),
                unit_price=Decimal(unit_price),
                supplier_payment_status=supplier_payment_status,
                payment_type=payment_type
            )

            print("===== STOCK CREATED SUCCESSFULLY =====")
            print(f"Stock ID: {stock.id}")

        except Exception as e:
            print("===== ERROR CREATING STOCK =====")
            print(str(e))
            raise

        return redirect('stock_list')

    return render(request, 'add_stock.html')


def stock_list(request):
    stocks = Stock.objects.all().order_by('-date_added')

    return render(
        request,
        'stock_list.html',
        {'stocks': stocks}
    )


def stock_receipt_list(request):
    receipts = StockReceipt.objects.all().order_by("-date_received")
    return render(request, "stock_receipt_list.html", {
        "receipts": receipts
    })


def create_stock_receipt(request):
    products = Stock.objects.all()

    if request.method == "POST":
        product = get_object_or_404(Stock, id=request.POST.get("product"))

        receipt = StockReceipt.objects.create(
            product=product,
            supplier_name=request.POST.get("supplier_name"),
            quantity_received=int(request.POST.get("quantity_received")),
            unit_cost=float(request.POST.get("unit_cost")),
            supplier_paid=request.POST.get("supplier_paid") == "on"
        )

        return redirect("goods_received_note", receipt_id=receipt.id)

    return render(request, "create_stock_receipt.html", {
        "products": products
    })


def goods_received_note(request, receipt_id):
    receipt = get_object_or_404(StockReceipt, id=receipt_id)

    return render(request, "goods_received_note.html", {
        "receipt": receipt
    })


def edit_stock_receipt(request, receipt_id):
    receipt = get_object_or_404(StockReceipt, id=receipt_id)
    products = Stock.objects.all()

    if request.method == "POST":
        product = get_object_or_404(Stock, id=request.POST.get("product"))

        receipt.product = product
        receipt.supplier_name = request.POST.get("supplier_name")
        receipt.quantity_received = int(request.POST.get("quantity_received"))
        receipt.unit_cost = float(request.POST.get("unit_cost"))
        receipt.supplier_paid = request.POST.get("supplier_paid") == "on"
        receipt.save()

        return redirect("goods_received_note", receipt_id=receipt.id)

    return render(request, "edit_stock_receipt.html", {
        "receipt": receipt,
        "products": products
    })


def delete_stock_receipt(request, receipt_id):
    receipt = get_object_or_404(StockReceipt, id=receipt_id)

    if request.method == "POST":
        receipt.delete()
        return redirect("stock_receipt_list")

    return render(request, "delete_stock_receipt.html", {
        "receipt": receipt
    })

#Views for sales
def sales_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales_list.html', {'sales': sales})



def add_sale(request):
    products = Stock.objects.all()

    if request.method == 'POST':

        print("\n========== FORM DATA ==========")
        print("customer_name:", request.POST.get('customer_name'))
        print("product:", request.POST.get('product'))
        print("quantity:", request.POST.get('quantity'))
        print("payment_method:", request.POST.get('payment_method'))
        print("distance_km:", request.POST.get('distance_km'))
        print("transport_required:", request.POST.get('transport_required'))
        print("FULL POST DATA:", request.POST)
        print("Hi")
        print("================================\n")

        product_id = request.POST.get('product')

        if not product_id:
            print("ERROR: No product selected")
            return render(
                request,
                'add_sale.html',
                {
                    'products': products,
                    'error': 'Please select a product.'
                }
            )

        product = get_object_or_404(Stock, id=product_id)

        print("Selected Product:", product)
        print("Product ID:", product.id)
        print("Available Quantity:", product.quantity_delivered)

        try:
            new_sale = Sale(
                customer_name=request.POST.get('customer_name'),
                product=product,
                quantity=int(request.POST.get('quantity')),
                payment_method=request.POST.get('payment_method'),
                distance_km=Decimal(request.POST.get('distance_km') or 0),
                transport_required=request.POST.get('transport_required') == 'on'
            )

            print("Sale object created successfully")

            new_sale.update_total_price()

            print("Sale saved successfully")
            print("Sale ID:", new_sale.id)
            print("Total Price:", new_sale.total_price)

            return redirect('sales_receipt', sale_id=new_sale.id)

        except Exception as e:
            print("ERROR OCCURRED:", str(e))
            raise

    return render(request, 'add_sale.html', {'products': products})

def sales_receipt(request, sale_id):
    sale = get_object_or_404(Sale, id=sale_id)
    return render(request, 'sales_receipt.html', {'sale': sale})

def edit_sale(request, sale_id):

    sale = get_object_or_404(Sale, id=sale_id)

    if request.method == 'POST':

        product = Stock.objects.get(id=request.POST.get('product'))

        sale.customer_name = request.POST.get('customer_name')
        sale.product = product
        sale.quantity = int(request.POST.get('quantity'))
        sale.payment_method = request.POST.get('payment_method')
        sale.distance_km = Decimal(request.POST.get('distance_km') or 0)

        sale.transport_required = request.POST.get('transport_required') == 'on'

        sale.update_total_price()

        return redirect('sales_list')

    products = Stock.objects.all()

    return render(request, 'edit_sale.html', {'sale': sale, 'products': products})

def stock_report(request):
    stocks = Stock.objects.annotate(
        quantity_sold=Coalesce(Sum('sale__quantity'), 0)
    ).annotate(
        remaining_quantity=F('quantity_delivered') - F('quantity_sold'),
        remaining_value=ExpressionWrapper(
            (F('quantity_delivered') - F('quantity_sold')) * F('unit_cost'),
            output_field=DecimalField(max_digits=12, decimal_places=2)
        )
    )

    return render(request, 'stock_report.html', {'stocks': stocks})


def sales_report(request):
    sales = Sale.objects.all().order_by("-date")

    start_date = request.GET.get("start_date")
    end_date = request.GET.get("end_date")

    if start_date:
        sales = sales.filter(date__gte=start_date)

    if end_date:
        sales = sales.filter(date__lte=end_date)

    total_sales_amount = sales.aggregate(
        total=Sum("total_price")
    )["total"] or 0

    total_quantity_sold = sales.aggregate(
        total=Sum("quantity")
    )["total"] or 0

    return render(request, "sales_report.html", {
        "sales": sales,
        "start_date": start_date,
        "end_date": end_date,
        "total_sales_amount": total_sales_amount,
        "total_quantity_sold": total_quantity_sold,
    })

def edit_stock(request, pk):
    stock = get_object_or_404(Stock, id=pk)

    if request.method == "POST":
        stock.supplier = request.POST.get("supplier")
        stock.category = request.POST.get("category")
        stock.product_name = request.POST.get("product_name")
        stock.quantity_delivered = int(request.POST.get("quantity_delivered"))
        stock.unit_cost = Decimal(request.POST.get("unit_cost"))
        stock.unit_price = Decimal(request.POST.get("unit_price"))
        stock.supplier_payment_status = request.POST.get("supplier_payment_status")
        stock.payment_type = request.POST.get("payment_type")

        stock.save()

        return redirect("stock_list")

    return render(request, "stock_edit.html", {"stock": stock})






