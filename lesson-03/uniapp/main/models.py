from django.conf import settings
from django.db import models


class Category(models.Model):
    title = models.CharField(max_length=200, unique=True)

    def __str__(self) -> str:
        return self.title


class Product(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField(blank=True, default="")
    price = models.PositiveIntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, related_name="products")

    def __str__(self) -> str:
        return self.title


class Profile(models.Model):
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="profile",
        null=True,
        blank=True,
    )
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    favorites = models.ManyToManyField(Product, blank=True, related_name="favorited_by")

    def __str__(self) -> str:
        return self.username
