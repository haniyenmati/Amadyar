import json
from typing import Optional, Iterable
from django.db import models
from django.utils.translation import gettext_lazy as _
from phonenumber_field.modelfields import PhoneNumberField
from accounts.models import User


class Company(models.Model):
    name = models.CharField(
        max_length=256, null=False, blank=False
    )
    company_code = models.CharField(
        max_length=64, null=False, blank=False, unique=True
    )
    support_phone_number = PhoneNumberField(
        unique=True, null=False, blank=False
    )

    def __str__(self) -> str:
        return self.company_code

    __repr__ = __str__


class Driver(models.Model):
    user: User = models.OneToOneField(
        User, on_delete=models.CASCADE, related_name='driver'
    )
    company: Company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='drivers_set'
    )

    @property
    def full_name(self):
        return self.user.full_name

    def __str__(self) -> str:
        return self.full_name

    __repr__ = __str__


class Storage(models.Model):
    label = models.CharField(
        max_length=256, null=False, blank=False
    )
    longtitude = models.FloatField(
        default=0, null=False, blank=False
    )
    latitude = models.FloatField(
        default=0, null=False, blank=False
    )
    owner_company: Company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='storages_set'
    )

    def __str__(self) -> str:
        return self.label

    __repr__ = __str__


class CarModel(models.Model):
    name = models.CharField(
        max_length=256, null=False, blank=False, unique=True
    )
    height = models.PositiveSmallIntegerField(null=False, blank=False)
    width = models.PositiveSmallIntegerField(null=False, blank=False)
    length = models.PositiveSmallIntegerField(null=False, blank=False)
    weight_capacity = models.PositiveSmallIntegerField(null=False, blank=False) # in kg

    def __str__(self) -> str:
        return self.name

    __repr__ = __str__


class Car(models.Model):
    plaque = models.CharField(
        max_length=64, null=False, blank=False, unique=True
    )
    car_model: CarModel = models.ForeignKey(
        CarModel, on_delete=models.CASCADE, related_name='cars_set'
    )
    owner_company: Company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name='cars_set'
    )
    extra_facilities = models.JSONField(default=dict)

    def __str__(self) -> str:
        return f'{self.plaque}'

    __repr__ = __str__


class Store(models.Model):
    name = models.CharField(
        max_length=256, null=False, blank=False
    )
    store_code = models.CharField(
        max_length=64, null=False, blank=False, unique=True
    )
    longtitude = models.FloatField(
        default=0, null=False, blank=False
    )
    latitude = models.FloatField(
        default=0, null=False, blank=False
    )
    owner_name = models.CharField(
        max_length=256, null=False, blank=False
    )

    def __str__(self) -> str:
        return f'{self.name}-{self.store_code}'

    __repr__ = __str__


class OrderStatus(models.TextChoices):
    ASSIGNED = 'AS', _('assigned')
    IN_PROGRESS = 'IP', _('in-progress')
    ARRIVED = 'AR', _('arrived')
    DELIVERED = 'DL', _('delivered')


class Order(models.Model):
    title = models.CharField(
        max_length=256, null=False, blank=False
    )
    # car: Car = models.ForeignKey(
    #     Car, on_delete=models.SET('deleted'), related_name='orders_set', null=True, blank=True
    # )
    driver: Driver = models.ForeignKey(
        Driver, on_delete=models.SET('deleted'), related_name='orders_set', default=1
    )
    origin: Storage = models.ForeignKey(
        Storage, on_delete=models.PROTECT, related_name='orders_set', null=True, blank=True
    )
    destination: Store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name='orders_set', null=True, blank=True
    )
    status: OrderStatus = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.ASSIGNED
    )
    weight = models.PositiveIntegerField(null=True, blank=True)
    start_tw = models.FloatField(null=True)
    end_tw = models.FloatField(null=True)
    estimation_arrival = models.FloatField(null=True)
    estimation_depart = models.FloatField(null=True)

    @property
    def end_time(self):
        end_time = self.logs_set.filter(action=LogAction.ENDED)
        if end_time.exists():
            return end_time.current_datetime
        return None

    @property
    def start_time(self):
        start_time = self.logs_set.filter(action=LogAction.STARTED)
        if start_time.exists():
            return start_time.current_datetime
        return None

    def __str__(self) -> str:
        return self.title

    __repr__ = __str__


class PathEstimation(models.Model):
    order: Order = models.ForeignKey(
        Order, on_delete=models.CASCADE, related_name='Paths'
    )
    longtitude = models.FloatField(
        default=0, null=False, blank=False
    )
    latitude = models.FloatField(
        default=0, null=False, blank=False
    )

    def __str__(self) -> str:
        return f'{self.pk}-{self.order.title}'

    __repr__ = __str__

class LogAction(models.TextChoices):
    STARTED = 'ST', _('started-trip')
    ENDED = 'ED', _('ended-trip')
    ON_THE_WAY = 'OW', _('on-the-way')
    TAKING_BREAK = 'TB', _('taking-break')
    DELIVERED = 'DV', _('delivered')
    CHARGE = 'CH', _('charging')
    DISCHARGE = 'DC', _('discharging')


class OrderLog(models.Model):
    related_order: Order = models.ForeignKey(
        Order, on_delete=models.PROTECT, related_name='logs_set'
    )
    longtitude = models.FloatField(
        default=0, null=False, blank=False
    )
    latitude = models.FloatField(
        default=0, null=False, blank=False
    )
    current_datetime = models.DateTimeField()
    action: LogAction = models.CharField(
        max_length=2, choices=LogAction.choices, default=LogAction.STARTED
    )

    def __str__(self) -> str:
        return f'{self.related_order} - {self.action}'

    __repr__ = __str__


class EstimationFiles(models.Model):
    orders = models.FileField(upload_to="static")
    routes = models.FileField(upload_to="static")
    uploaded_at = models.DateTimeField(auto_now_add=True)

    def save(self, force_insert: bool = ..., force_update: bool = ..., using: Optional[str] = ..., update_fields: Optional[Iterable[str]] = ...) -> None:
        ret = super().save()

        with open(self.orders.path, 'r') as jfo:
            orders = json.load(jfo)['features']

        with open(self.routes.path, 'r') as jfr:
            routes = json.load(jfr)['features']

        for route in routes:
            print(route)
            route_name = route['attributes']['Name']
            orders_with_according_route = list(filter(lambda o: o['attributes']['RouteName'] == route_name, orders))

            paths = route['geometry']['paths']
            driver = Driver.objects.last()

            for path in paths:
                path_order = orders_with_according_route[paths.index(path)-1]
                order = Order(
                    driver=driver,
                    title=path_order['attributes']['Name'],
                    estimation_arrival=path_order['attributes']['ArriveTimeUTC'],
                    estimation_depart=path_order['attributes']['DepartTimeUTC'],
                    start_tw=path_order['attributes']['TimeWindowStart1'],
                    end_tw=path_order['attributes']['TimeWindowEnd1']
                )
                order.save()

                for location in path:
                    ope = PathEstimation(
                        order=order,
                        latitude=location[1],
                        longtitude=location[0],
                    )
                    ope.save()
        return ret

    def __str__(self) -> str:
        return f'{self.uploaded_at}'

    __repr__ = __str__
