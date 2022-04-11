from django.urls import path
from haul.views import OrderPathEstimationView, OrdersView, UncompletedOrdersView

app_name = 'haul'

urlpatterns = [
    path('order/', OrdersView.as_view(), name='orders'),
    path('order/uncompleted/', UncompletedOrdersView.as_view(), name='uncompleted_orders'),
    path('order/<int:order_pk>/path/estimation/', OrderPathEstimationView.as_view(), name='order_path_estimation'),
]
