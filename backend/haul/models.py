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
    longtitude = models.PositiveIntegerField(
        default=0, null=False, blank=False
    )
    latitude = models.PositiveIntegerField(
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
    longtitude = models.PositiveIntegerField(
        default=0, null=False, blank=False
    )
    latitude = models.PositiveIntegerField(
        default=0, null=False, blank=False
    )
    owner_name = models.CharField(
        max_length=256, null=False, blank=False
    )

    def __str__(self) -> str:
        return f'{self.name}-{self.store_code}'

    __repr__ = __str__


class OrderStatus(models.TextChoices):
    COMPLETE = 'CP', _('complete')
    IN_PROGRESS = 'IP', _('in-progress')
    BACKLOG = 'BL', _('backlog')
    MISSED = 'MS', _('missed')


class Order(models.Model):
    title = models.CharField(
        max_length=256, null=False, blank=False
    )
    car: Car = models.ForeignKey(
        Car, on_delete=models.SET('deleted'), related_name='orders_set'
    )
    origin: Storage = models.ForeignKey(
        Storage, on_delete=models.PROTECT, related_name='orders_set'
    )
    destination: Store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name='orders_set'
    )
    status: OrderStatus = models.CharField(
        max_length=2, choices=OrderStatus.choices, default=OrderStatus.BACKLOG
    )
    weight = models.PositiveIntegerField()
    start_tw = models.DateTimeField()
    end_tw = models.DateTimeField()

    def __str__(self) -> str:
        return self.title

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
    longtitude = models.PositiveIntegerField(
        default=0, null=False, blank=False
    )
    latitude = models.PositiveIntegerField(
        default=0, null=False, blank=False
    )
    current_datetime = models.DateTimeField()
    action: LogAction = models.CharField(
        max_length=2, choices=LogAction.choices, default=LogAction.STARTED
    )

    def __str__(self) -> str:
        return f'{self.related_order} - {self.action}'

    __repr__ = __str__
