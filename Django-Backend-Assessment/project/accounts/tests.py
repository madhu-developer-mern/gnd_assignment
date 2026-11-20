from django.contrib.auth.hashers import check_password
from django.db import IntegrityError, transaction
from rest_framework.test import APITestCase

from .models import Account


class RegistrationTests(APITestCase):
    url = "/api/register/"
    sample = {
        "name": " Madhu ",
        "email": "MADHU@example.com",
        "phone_number": "0987654321",
        "password": "Password@123",
    }

    def register(self, **changes):
        return self.client.post(self.url, {**self.sample, **changes}, format="json")

    def test_register_trims_normalizes_and_hashes(self):
        response = self.register()
        self.assertEqual(response.status_code, 201)
        account = Account.objects.get()
        self.assertEqual(response.json(), {
            "id": account.pk, "name": "Madhu", "email": "madhu@example.com",
            "phone_number": "0987654321", "message": "User registered successfully",
        })
        self.assertEqual((account.name, account.email, account.phone_number),
                         ("Madhu", "madhu@example.com", "0987654321"))
        self.assertNotEqual(account.password, self.sample["password"])
        self.assertTrue(check_password(self.sample["password"], account.password))

    def test_missing_fields(self):
        response = self.client.post(self.url, {}, format="json")
        self.assertEqual(response.status_code, 400)
        self.assertEqual(set(response.json()), set(self.sample))

    def test_rejects_invalid_field_values(self):
        invalid = {
            "name": ["", "   ", "a" * 21, 12],
            "email": ["not-an-email", "a" * 65 + "@" + "b" * 25 + ".example.com"],
            "phone_number": ["123456789", "12345678901", "12345abcde",
                             "1234567890\n", "１２３４５６７８９０", 1234567890],
            "password": ["Ab1!", "A1!" + "a" * 28, "password@123", "PASSWORD@123",
                         "Password@abc", "Password123", "Password 123"],
        }
        for field, values in invalid.items():
            for value in values:
                with self.subTest(field=field, value=value):
                    response = self.register(**{field: value})
                    self.assertEqual(response.status_code, 400)
                    self.assertIn(field, response.json())
        self.assertFalse(Account.objects.exists())

    def test_accepts_inclusive_length_boundaries(self):
        first = self.register(name=" X ", password="Abcdef1!")
        self.assertEqual(first.status_code, 201)
        second = self.register(
            name="X" * 20, password="A1!" + "a" * 27,
            email="a" * 60 + "@" + "b" * 35 + ".com",
            phone_number="1234567890",
        )
        self.assertEqual(second.status_code, 201)

    def test_reports_email_and_phone_conflicts_independently(self):
        self.assertEqual(self.register().status_code, 201)
        for changes, fields in [
            ({"email": "madhu@EXAMPLE.com", "phone_number": "1234567890"}, {"email"}),
            ({"email": "different@example.com"}, {"phone_number"}),
            ({"email": "madhu@example.com"}, {"email", "phone_number"}),
        ]:
            with self.subTest(fields=fields):
                response = self.register(**changes)
                self.assertEqual(response.status_code, 400)
                self.assertEqual(set(response.json()), fields)
        self.assertEqual(Account.objects.count(), 1)

    def test_database_enforces_case_insensitive_email_and_unique_phone(self):
        self.assertEqual(self.register().status_code, 201)
        for email, phone in [("MADHU@example.com", "1234567890"),
                             ("different@example.com", self.sample["phone_number"])]:
            with self.subTest(email=email), self.assertRaises(IntegrityError), transaction.atomic():
                Account.objects.create(name="Other", email=email, phone_number=phone,
                                       password="not-a-real-password-hash")

    def test_rejects_malformed_json(self):
        response = self.client.post(self.url, "{", content_type="application/json")
        self.assertEqual(response.status_code, 400)
