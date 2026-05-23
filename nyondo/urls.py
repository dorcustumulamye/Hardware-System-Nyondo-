from django.urls import path
from . import views

urlpatterns = [
  path('', views.sales_list, name='sales_list'),
  path('add_sale/', views.add_sale, name='add_sale'),
  path('sales_receipt/<int:sale_id>/', views.sales_receipt, name='sales_receipt'),
  path('edit_sale/<int:sale_id>/', views.edit_sale, name='edit_sale'),
  path('stock_list/', views.stock_list, name='stock_list'),
  path('add_stock/', views.add_stock, name='add_stock'),
  path('sales_list/', views.sales_list, name='sales_list'),
  path('stock_report/', views.stock_report, name='stock_report'),
]