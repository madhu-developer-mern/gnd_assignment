"""Version 1 catalog used by the data migration."""

from decimal import Decimal

# Name, description, category, brand, price, discount, stock, rating, available.
PRODUCTS_V1 = (
    ("Wireless Headphones", "Bluetooth wireless headphones", "Electronics", "Sony", 4999, 10, 25, "4.50", True),
    ("Laptop", "14-inch laptop for work and study", "Electronics", "Lenovo", 54999, 12, 8, "4.70", True),
    ("Smartphone", "Unlocked smartphone with OLED display", "Electronics", "Samsung", 22999, 8, 12, "4.30", True),
    ("Smart Watch", "Fitness watch with heart-rate tracking", "Electronics", "Amazfit", 6999, 15, 18, "4.20", True),
    ("Keyboard", "Full-size wired keyboard", "Electronics", "Logitech", 1799, 5, 32, "4.00", True),
    ("Mouse", "Compact wireless mouse", "Electronics", "Logitech", 999, 0, 0, "3.80", False),
    ("Running Shoes", "Lightweight mesh running shoes", "Sports", "Nike", 3499, 20, 14, "4.40", True),
    ("T-Shirt", "Crew-neck cotton T-shirt", "Fashion", "Uniqlo", 699, 5, 40, "4.10", True),
    ("Backpack", "Water-resistant everyday backpack", "Fashion", "Wildcraft", 1599, 10, 17, "4.20", True),
    ("Coffee Maker", "Drip coffee maker with glass carafe", "Home", "Philips", 3299, 12, 9, "4.30", True),
    ("Office Chair", "Adjustable mesh office chair", "Home", "IKEA", 7999, 15, 4, "4.40", True),
    ("Python Programming Book", "Introduction to Python fundamentals", "Books", "O'Reilly", 1299, 10, 20, "4.80", True),
    ("Cricket Bat", "English willow cricket bat", "Sports", "SG", 2599, 10, 6, "4.20", True),
    ("Face Wash", "Daily facial cleanser", "Beauty", "Cetaphil", 399, 0, 30, "4.00", True),
    ("Water Bottle", "Insulated steel water bottle", "Sports", "Milton", 649, 5, 21, "4.30", True),
    ("Sunscreen", "Broad-spectrum SPF 50 sunscreen", "Beauty", "Neutrogena", 599, 10, 0, "4.10", True),
    ("Desk Lamp", "Dimmable LED reading lamp", "Home", "Philips", 1399, 5, 10, "3.90", True),
    ("Mystery Novel", "Paperback detective novel", "Books", "Penguin", 449, 0, 13, "4.50", True),
    ("Denim Jacket", "Classic button-front denim jacket", "Fashion", "Levi's", 2899, 20, 0, "4.20", False),
    ("Yoga Mat", "Textured yoga mat with carry strap", "Sports", "Decathlon", 1199, 5, 16, "4.00", True),
)


def seed_catalog(apps, schema_editor):
    item_model = apps.get_model("products", "Item")
    insert_sample_items(item_model.objects.using(schema_editor.connection.alias))


def insert_sample_items(items):
    for item_id, product in enumerate(PRODUCTS_V1, start=1):
        name, description, category, brand, price, discount, stock, rating, available = product
        items.get_or_create(
            pk=item_id,
            defaults={
                "name": name, "description": description, "category": category, "brand": brand,
                "price": Decimal(price), "discount_percentage": discount, "stock_quantity": stock,
                "rating": Decimal(rating), "is_available": available,
            },
        )
