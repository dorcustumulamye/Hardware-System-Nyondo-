from decimal import Decimal
from django.db.models import Sum, F, ExpressionWrapper, DecimalField
from django.db.models.functions import Coalesce
from django.shortcuts import render, redirect, get_object_or_404
from .models import Sale, Stock



# Create your views here.

#Views for stock management
def add_stock(request):

    if request.method == 'POST':

        Stock.objects.create(
            supplier=request.POST.get('supplier'),
            category=request.POST.get('category'),
            product_name=request.POST.get('product_name'),
            quantity_delivered=int(request.POST.get('quantity_delivered')),
            unit_cost=Decimal(request.POST.get('unit_cost')),
            unit_price=Decimal(request.POST.get('unit_price')),
            supplier_payment_status=request.POST.get('supplier_payment_status'),
            payment_type=request.POST.get('payment_type')
        )

        return redirect('stock_list')

    return render(request, 'add_stock.html')


def stock_list(request):

    stocks = Stock.objects.all().order_by('-date_added')

    return render(
        request,
        'stock_list.html',
        {'stocks': stocks}
    )



#Views for sales
def sales_list(request):
    sales = Sale.objects.all().order_by('-date')
    return render(request, 'sales_list.html', {'sales': sales})

def add_sale(request):
    products = Stock.objects.all()

    if request.method == 'POST':
        product_id = request.POST.get('product')

        if not product_id:
            return render(request, 'add_sale.html', {'products': products, 'error': 'Please select a product.'})

        product = get_object_or_404(Stock, id=product_id)


        new_sale = Sale(
            customer_name = request.POST.get('customer_name'),
            product = product,
            quantity = int(request.POST.get('quantity')),
            payment_method = request.POST.get('payment_method'),
            distance_km = Decimal(request.POST.get('distance_km', 0)),
            transport_required = request.POST.get('transport_required') == 'on'
      
        )
  
        new_sale.update_total_price()

        return redirect('sales_receipt', sale_id=new_sale.id)

    products = Stock.objects.all()
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




