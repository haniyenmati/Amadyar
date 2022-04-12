from django.urls import path
from haul.views import OrderPathEstimationView, OrdersView, UncompletedOrdersView, ChangeOrderStatus, NextOrderView

app_name = 'haul'

urlpatterns = [
    path('next_order/', NextOrderView.as_view(), name='next_order'),
    path('order/', OrdersView.as_view(), name='orders'),
    path('order/uncompleted/', UncompletedOrdersView.as_view(), name='uncompleted_orders'),
    path('order/<int:order_pk>/path/estimation/', OrderPathEstimationView.as_view(), name='order_path_estimation'),
    path('order/change_status/<int:order_pk>/', ChangeOrderStatus.as_view(), name='change_order_status')
]
