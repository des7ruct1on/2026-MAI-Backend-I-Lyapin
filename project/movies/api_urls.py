from django.urls import path

from movies.api_views import (
    add_to_favorites,
    category_page,
    movies_create,
    movies_feed,
    profile,
    search,
)


urlpatterns = [
    path("profile/", profile, name="api_profile"),
    path("search/", search, name="api_search"),
    path("movies/", movies_feed, name="api_movies_feed"),
    path("movies/create", movies_create, name="api_movies_create"),
    path("categories/<int:category_id>/", category_page, name="api_category_page"),
    path("favorites/add/", add_to_favorites, name="api_favorites_add"),
]

