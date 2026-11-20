from django.core.management.base import BaseCommand
from django.db import transaction

from products.models import Item
from products.seed import PRODUCTS_V1, insert_sample_items


class Command(BaseCommand):
    help = "Load the sample catalog when the products table is empty."

    def handle(self, *args, **options):
        items = Item.objects.all()
        if items.exists():
            self.stdout.write("Catalog already contains products.")
            return

        with transaction.atomic():
            insert_sample_items(items)
        self.stdout.write(f"Sample catalog loaded ({len(PRODUCTS_V1)} products).")
