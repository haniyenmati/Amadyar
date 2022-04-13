from django.db.models import Q
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from haul.models import Order, Driver, OrderStatus, OrderLog
from haul.serializers import OrderSerializer, OrderPathsSerializer, ChangeOrderStatusSerializer, \
    OrderLogsListSerializer
from rest_framework.response import Response
from rest_framework.generics import ListAPIView, GenericAPIView


# Create your views here.
class NextOrderView(APIView):
    serializer_class = OrderPathsSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        qs = Order.objects.filter(driver=driver).filter(~Q(status=OrderStatus.DELIVERED)).order_by('estimation_arrival')
        return qs.first()

    def get(self, request, *args, **kwargs):
        qs = self.get_queryset()
        if qs:
            ser = self.serializer_class(qs)
            return Response(ser.data, status=status.HTTP_200_OK)
        return Response(status=status.HTTP_404_NOT_FOUND)


class OrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        # TODO get date or day numbers from query param and filter items by that time
        return Order.objects.filter(driver=driver)


class UncompletedOrdersView(ListAPIView):
    serializer_class = OrderSerializer
    permission_classes = [IsAuthenticated]

    def get_queryset(self):
        user = self.request.user
        driver = Driver.objects.get(user=user)
        # TODO filter estimation today
        return Order.objects.filter(driver=driver).filter(~Q(status=OrderStatus.DELIVERED)).order_by(
            'estimation_arrival')


class ChangeOrderStatus(GenericAPIView):
    serializer_class = ChangeOrderStatusSerializer

    def post(self, request, *args, **kwargs):
        serializer = ChangeOrderStatusSerializer(data=request.data)

        try:
            serializer.is_valid(raise_exception=True)
            order = Order.objects.get(id=kwargs.get('order_pk'))
            ret = order.change_order_status(to=serializer.validated_data['status'])
            return Response({"new_status": ret})

        except Exception as err:
            return Response({"detail": f"{err}"}, status=400)


class CreateOrderLogsList(GenericAPIView):
    serializer_class = OrderLogsListSerializer

    def post(self, request, *args, **kwargs):
        order_pk = kwargs.get('order_pk')

        try:
            OrderLog.create_logs_from_list(order_pk=order_pk, logs=request.data["logs"])
            return Response({"ok": True})

        except Exception as err:
            return Response({"detail": f"{err}"}, status=400)
