from django.core.management.base import BaseCommand
from haul.models import Order
from openpyxl import Workbook


class Command(BaseCommand):
    help = 'Get list of orderlogs'

    def add_arguments(self, parser) -> None:
        parser.add_argument('--order_id', type=int, help='order id/pk', default=None)

    def handle(self, *args, **options):
        order_pk = options['order_id']
        order = Order.objects.get(id=order_pk)

        wb = Workbook()
        ws = wb.active 

        for log in order.logs_set.all():
            print(log)