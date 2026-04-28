from __future__ import annotations

import json

from django.http import JsonResponse, HttpRequest
from django.db.models import Q
from django.views.decorators.http import require_http_methods

from movies.models import Movie, Genre

@require_http_methods(["GET"])
def profile(request: HttpRequest) -> JsonResponse:
    return JsonResponse(
        {
            "profile": {
                "id": 1,
                "username": "stub-user",
                "favorites_count": 0,
            }
        }
    )


@require_http_methods(["GET"])
def movies_feed(request: HttpRequest) -> JsonResponse:
    movies = Movie.objects.select_related("genre").all().order_by("-added_at")
    return JsonResponse({"movies": [_serialize_movie(m) for m in movies]})


def _serialize_movie(movie: Movie) -> dict:
    return {
        "id": movie.id,
        "title": movie.title,
        "description": movie.description,
        "year": movie.year,
        "genre": (
            {"id": movie.genre.id, "name": movie.genre.name} if movie.genre_id else None
        ),
        "added_at": movie.added_at.isoformat() if movie.added_at else None,
    }


@require_http_methods(["GET"])
def search(request: HttpRequest) -> JsonResponse:
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"q": q, "movies": []})

    movies = (
        Movie.objects.select_related("genre")
        .filter(Q(title__icontains=q) | Q(description__icontains=q))
        .order_by("-added_at")
    )
    return JsonResponse({"q": q, "movies": [_serialize_movie(m) for m in movies]})


@require_http_methods(["POST"])
def movies_create(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"ok": False, "error": "invalid_json"}, status=400)

    title = (payload.get("title") or "").strip()
    if not title:
        return JsonResponse({"ok": False, "error": "title_required"}, status=400)

    description = (payload.get("description") or "").strip()
    year = payload.get("year")
    genre_id = payload.get("genre_id")

    genre = None
    if genre_id is not None:
        try:
            genre = Genre.objects.get(id=int(genre_id))
        except (ValueError, Genre.DoesNotExist):
            return JsonResponse({"ok": False, "error": "genre_not_found"}, status=400)

    movie = Movie.objects.create(
        title=title,
        description=description,
        year=int(year) if year is not None else None,
        genre=genre,
    )
    return JsonResponse({"ok": True, "movie": _serialize_movie(movie)}, status=201)


@require_http_methods(["GET"])
def category_page(request: HttpRequest, category_id: int) -> JsonResponse:
    return JsonResponse(
        {
            "category": {"id": category_id, "name": "Stub category"},
            "movies": [],
        }
    )


@require_http_methods(["POST"])
def add_to_favorites(request: HttpRequest) -> JsonResponse:
    try:
        payload = json.loads(request.body.decode("utf-8") or "{}")
    except json.JSONDecodeError:
        payload = {}

    return JsonResponse(
        {
            "ok": True,
            "received": payload,
        }
    )

