from rest_framework.generics import ListAPIView

from haul.models import PathEstimation, Order, Driver
from haul.serializers import PathEstimationSerializer, OrderSerializer


# Create your views here.
class OrderPathEstimationView(ListAPIView):
    serializer_class = PathEstimationSerializer

    def get_queryset(self):
        return PathEstimation.objects.filter(order_id=self.kwargs['order_pk']).order_by('id')


class OrdersView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        # TODO get date or day numbers from query param and filter items by that time
        return Order.objects.filter(driver=driver)


class UncompletedOrdersView(ListAPIView):
    serializer_class = OrderSerializer

    def get_queryset(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        # TODO return items which are not completed
        return Order.objects.filter(driver=driver)
