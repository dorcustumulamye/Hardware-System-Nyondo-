from django.urls import path
from . import views

urlpatterns = [
  path('', views.sales_list, name='sales_list'),
  path('add_sale/', views.add_sale, name='add_sale'),
  path('sales_receipt/<int:sale_id>/', views.sales_receipt, name='sales_receipt'),
  path('edit_sale/<int:sale_id>/', views.edit_sale, name='edit_sale'),
  path("sales/report/", views.sales_report, name="sales_report"),

  path('stock/', views.stock_list, name='stock_list'),
  path('add_stock/', views.add_stock, name='add_stock'),
  path('stock_report/', views.stock_report, name='stock_report'),
  path("receipts/", views.stock_receipt_list, name="stock_receipt_list"),
  path("receipts/create/", views.create_stock_receipt, name="create_stock_receipt"),
  path("receipts/<int:receipt_id>/grn/", views.goods_received_note, name="goods_received_note"),
  path("receipts/<int:receipt_id>/edit/", views.edit_stock_receipt, name="edit_stock_receipt"),
  path("receipts/<int:receipt_id>/delete/", views.delete_stock_receipt, name="delete_stock_receipt"),
  path('edit_stock/<int:pk>/', views.edit_stock, name='edit_stock'),
]