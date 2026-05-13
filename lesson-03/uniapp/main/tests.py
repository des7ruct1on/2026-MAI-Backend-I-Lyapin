import json

from django.test import Client, TestCase

from .models import Category, Product


class ProductApiTests(TestCase):
    def setUp(self):
        self.client = Client(enforce_csrf_checks=False)
        self.cat = Category.objects.create(title="Books")
        Product.objects.create(
            title="Silence of the Lambs",
            description="Thriller movie",
            price=100,
            category=self.cat,
        )
        Product.objects.create(
            title="Other item",
            description="This description mentions silence",
            price=50,
            category=self.cat,
        )

    def test_search_requires_q(self):
        r = self.client.get("/api/search/")
        self.assertEqual(r.status_code, 400)

    def test_search_matches_title_or_description(self):
        r = self.client.get("/api/search/", {"q": "silence"})
        self.assertEqual(r.status_code, 200)
        data = r.json()
        self.assertEqual(len(data["items"]), 2)

    def test_products_list_get_only(self):
        r = self.client.get("/api/products/")
        self.assertEqual(r.status_code, 200)
        self.assertGreaterEqual(len(r.json()["items"]), 2)
        r2 = self.client.post("/api/products/", {}, content_type="application/json")
        self.assertEqual(r2.status_code, 405)

    def test_products_create_post_only(self):
        r = self.client.get("/api/products/create/")
        self.assertEqual(r.status_code, 405)

    def test_products_create(self):
        payload = {
            "title": "New",
            "description": "d",
            "price": 10,
            "category_id": self.cat.id,
        }
        r = self.client.post(
            "/api/products/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(r.json()["title"], "New")
        self.assertEqual(Product.objects.filter(title="New").count(), 1)

    def test_products_create_by_category_title(self):
        payload = {
            "title": "Gadget",
            "description": "",
            "price": 1,
            "category_title": "Electronics",
        }
        r = self.client.post(
            "/api/products/create/",
            data=json.dumps(payload),
            content_type="application/json",
        )
        self.assertEqual(r.status_code, 201)
        self.assertEqual(Category.objects.filter(title="Electronics").count(), 1)
        self.assertEqual(Product.objects.get(title="Gadget").category.title, "Electronics")
