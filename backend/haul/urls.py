from django.urls import path
from haul.views import NextOrderView, OrdersView, UncompletedOrdersView

app_name = 'haul'

urlpatterns = [
    path('next_order/', NextOrderView.as_view(), name='next_order'),
    path('order/', OrdersView.as_view(), name='orders'),
    path('order/uncompleted/', UncompletedOrdersView.as_view(), name='uncompleted_orders'),
]
