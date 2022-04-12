from rest_framework import serializers

from haul.models import PathEstimation, OrderLog, Order, OrderStatus


class PathEstimationSerializer(serializers.ModelSerializer):
    class Meta:
        model = PathEstimation
        fields = '__all__'


class OrderLogSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderLog
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'

class OrderPathsSerializer(serializers.ModelSerializer):
    paths = PathEstimationSerializer(read_only=True, many=True)
    start_time = serializers.DateTimeField(read_only=True)
    end_time = serializers.DateTimeField(read_only=True)

    class Meta:
        model = Order
        fields = '__all__'
class ChangeOrderStatusSerializer(serializers.Serializer):
    status = serializers.ChoiceField(choices=OrderStatus.choices)
