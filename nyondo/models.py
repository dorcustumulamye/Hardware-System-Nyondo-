from django.db import models
from decimal import Decimal
from django.utils import timezone


# Create your models here.
class Stock(models.Model):
    PAYMENT_STATUS_CHOICES = [('Paid', 'Paid'), ('Not Paid', 'Not Paid')]
    PAYMENT_TYPE_CHOICES = [('Cash', 'Cash'), ('Mobile Money', 'Mobile Money'), ('Bank Transfer', 'Bank Transfer'), ('Credit', 'Credit')]

    supplier = models.CharField(max_length=100)
    category = models.CharField(max_length=100)
    product_name = models.CharField(max_length=100)
    quantity_delivered = models.PositiveIntegerField(default=0)
    unit_cost = models.DecimalField(max_digits=10, decimal_places=2)
    total_value_goods = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    supplier_payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS_CHOICES, default='Not Paid')
    payment_type = models.CharField(max_length=50, choices=PAYMENT_TYPE_CHOICES, blank=True, null=True)
    date_added = models.DateTimeField(default=timezone.now)

    def save(self, *args, **kwargs):
        self.total_value_goods = self.quantity_delivered * self.unit_cost
        super().save(*args, **kwargs)

    def __str__(self):
        return self.product_name


class Sale(models.Model):
    customer_name = models.CharField(max_length=100)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE, default=None)
    quantity = models.PositiveIntegerField()
    sub_total = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    date = models.DateTimeField(default=timezone.now)
    payment_method = models.CharField(max_length=50)
    distance_km = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    transport_required = models.BooleanField(default=False)
    transport_fee = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2, default=0)

    def update_total_price(self):
        self.sub_total = self.quantity * self.product.unit_price

        if self.transport_required:
            if self.distance_km <= Decimal('10') and self.sub_total >= Decimal('500000'):
                self.transport_fee = Decimal('0.00')
            else:
                self.transport_fee = Decimal('30000')
        else:
            self.transport_fee = Decimal('0.00')

        self.total_price = self.sub_total + self.transport_fee
        self.product.save()

        self.save()

    def __str__(self):
        return f"{self.customer_name} - {self.product.product_name}"




