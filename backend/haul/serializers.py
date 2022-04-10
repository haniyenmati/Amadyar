from rest_framework import serializers

from haul.models import PathEstimation, OrderLog, Order


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
