from django.db import models
from nyondo.models import Stock, Sale

# Create your models here.
class SchemeCustomer(models.Model):
    full_name = models.CharField(max_length=150)
    nin_number = models.CharField(max_length=14, unique=True)
    phone_number = models.CharField(max_length=10)
    address = models.TextField()
    occupation = models.CharField(max_length=100, default="Salary Earner")
    employer_name = models.CharField(max_length=150, blank=True)
    date_registered = models.DateTimeField(auto_now_add=True)

   

    def __str__(self):
        return self.full_name


class SchemePayment(models.Model):
    customer = models.ForeignKey(SchemeCustomer, on_delete=models.CASCADE)
    amount_paid = models.DecimalField(max_digits=12, decimal_places=2)
    payment_date = models.DateTimeField(auto_now_add=True)
    notes = models.TextField(blank=True)

    def __str__(self):
        return f"{self.customer.full_name} - {self.amount_paid}"


class SchemeGoodsPickup(models.Model):
    customer = models.ForeignKey(SchemeCustomer, on_delete=models.CASCADE)
    product = models.ForeignKey(Stock, on_delete=models.CASCADE)
    quantity_taken = models.PositiveIntegerField()
    linked_sale = models.ForeignKey(Sale, on_delete=models.SET_NULL, null=True, blank=True)
    pickup_date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.customer.full_name} - {self.product.product_name}"

