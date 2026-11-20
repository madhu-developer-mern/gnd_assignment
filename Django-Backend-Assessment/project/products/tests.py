import json
from types import SimpleNamespace

from django.apps import apps
from django.db import connection
from rest_framework.test import APITestCase

from .models import Item
from .seed import seed_catalog


class CatalogSetupTests(APITestCase):
    def test_catalog_is_seeded_and_idempotent(self):
        self.assertEqual(Item.objects.count(), 20)
        self.assertEqual(set(Item.objects.values_list("category", flat=True)), {
            "Electronics", "Fashion", "Sports", "Books", "Home", "Beauty",
        })
        seed_catalog(apps, SimpleNamespace(connection=connection))
        self.assertEqual(Item.objects.count(), 20)

    def test_method_routing(self):
        response = self.client.options("/api/items/")
        self.assertEqual(response.status_code, 200)
        self.assertEqual(set(response.headers["Allow"].split(", ")),
                         {"GET", "HEAD", "OPTIONS", "QUERY"})
        self.assertEqual(self.client.post("/api/items/", {}, format="json").status_code, 405)


class ItemTests(APITestCase):
    url = "/api/items/"
    item_fields = {
        "id", "name", "description", "category", "brand", "price", "discount_percentage",
        "stock_quantity", "rating", "is_available", "created_at", "updated_at",
    }

    def query(self, body):
        return self.client.generic("QUERY", self.url, json.dumps(body),
                                   content_type="application/json")

    def test_get_all_items(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        items = response.json()
        self.assertEqual(len(items), 20)
        self.assertEqual(set(items[0]), self.item_fields)
        self.assertEqual(items[0]["price"], 4999)
        self.assertEqual(items[0]["rating"], 4.5)
        self.assertEqual(items[0]["name"], "Wireless Headphones")

    def test_get_pagination(self):
        expected_ids = list(Item.objects.values_list("id", flat=True))
        for qs, expected in [
            ("page=1&page_size=10", expected_ids[:10]),
            ("page=2&page_size=10", expected_ids[10:]),
            ("page=3", []), ("page=1", expected_ids[:10]),
            ("page_size=1", expected_ids[:1]), ("page_size=100", expected_ids),
            ("page=999999999999999999999", []),
        ]:
            with self.subTest(query_string=qs):
                response = self.client.get(f"{self.url}?{qs}")
                self.assertEqual(response.status_code, 200)
                self.assertEqual([item["id"] for item in response.json()], expected)

    def test_get_rejects_invalid_pagination(self):
        for key, value in [("page", 0), ("page", "x"), ("page", 1.5),
                           ("page_size", 0), ("page_size", 101), ("page_size", "")]:
            with self.subTest(key=key, value=value):
                response = self.client.get(self.url, {key: value})
                self.assertEqual(response.status_code, 400)
                self.assertIn(key, response.json())

    def test_query_all_items(self):
        for response in (self.query({}), self.client.generic("QUERY", self.url)):
            self.assertEqual(response.status_code, 200)
            self.assertEqual(response.json()["total"], 20)
            self.assertEqual(response.json()["items"], self.client.get(self.url).json())

    def test_query_filters(self):
        for body, names in [
            ({"name": "HeAdPhOnEs"}, ["Wireless Headphones"]),
            ({"category": "eLeCtRoNiCs"}, ["Wireless Headphones", "Laptop",
                                          "Smartphone", "Smart Watch", "Keyboard", "Mouse"]),
            ({"brand": "loGiTeCH"}, ["Keyboard", "Mouse"]),
            ({"min_price": 4999, "max_price": 4999}, ["Wireless Headphones"]),
            ({"min_rating": 4.5, "max_rating": 4.5}, ["Wireless Headphones", "Mystery Novel"]),
            ({"min_discount": 20, "max_discount": 20}, ["Running Shoes", "Denim Jacket"]),
            ({"in_stock": False}, ["Mouse", "Sunscreen", "Denim Jacket"]),
            ({"is_available": False}, ["Mouse", "Denim Jacket"]),
            ({"in_stock": True, "is_available": False}, []),
            ({"category": "Electronics", "min_price": 2000, "max_price": 10000,
              "min_rating": 4, "in_stock": True, "is_available": True},
             ["Wireless Headphones", "Smart Watch"]),
        ]:
            with self.subTest(body=body):
                response = self.query(body)
                self.assertEqual(response.status_code, 200)
                result = response.json()
                self.assertEqual(result["total"], len(names))
                self.assertEqual([item["name"] for item in result["items"]], names)

    def test_query_validation(self):
        for body, field in [
            ([], "non_field_errors"), (None, "non_field_errors"),
            ({"min_price": 20, "max_price": 10}, "max_price"),
            ({"min_rating": 4.5, "max_rating": 4}, "max_rating"),
            ({"min_discount": 20, "max_discount": 10}, "max_discount"),
            ({"max_rating": 6}, "max_rating"), ({"min_discount": -1}, "min_discount"),
            ({"max_price": "bad"}, "max_price"), ({"in_stock": "true"}, "in_stock"),
            ({"is_available": 1}, "is_available"), ({"extra": "x"}, "extra"),
        ]:
            with self.subTest(body=body):
                response = self.query(body)
                self.assertEqual(response.status_code, 400)
                self.assertIn(field, response.json())
        broken = self.client.generic("QUERY", self.url, "{", content_type="application/json")
        self.assertEqual(broken.status_code, 400)

    def test_query_is_read_only(self):
        before = list(Item.objects.values())
        self.assertEqual(self.query({"in_stock": True}).status_code, 200)
        self.assertEqual(self.query({"name": "irrelevant"}).status_code, 200)
        self.assertEqual(list(Item.objects.values()), before)
