from django.urls import path

from . import views

urlpatterns = [
    path("profile/", views.api_profile, name="api_profile"),
    path("search/", views.api_search, name="api_search"),
    path("products/create/", views.api_products_create, name="api_products_create"),
    path("products/", views.api_products, name="api_products"),
    path("category/<int:category_id>/", views.api_category, name="api_category"),
    path("favorites/add/", views.api_favorites_add, name="api_favorites_add"),
]
