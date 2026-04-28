from __future__ import annotations

from django.http import JsonResponse, HttpRequest, HttpResponse
from django.shortcuts import get_object_or_404
from django.views.decorators.http import require_http_methods

from movies.models import Movie


def _serialize_movie(movie: Movie) -> dict:
    return {
        "id": movie.id,
        "title": movie.title,
        "year": movie.year,
        "genre": (
            {"id": movie.genre.id, "name": movie.genre.name} if movie.genre_id else None
        ),
        "added_at": movie.added_at.isoformat() if movie.added_at else None,
    }


@require_http_methods(["GET"])
def movie_index(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Movies app")


@require_http_methods(["GET"])
def movies_list(request: HttpRequest) -> JsonResponse:
    movies = Movie.objects.all()
    return JsonResponse({"movies": [_serialize_movie(m) for m in movies]})


@require_http_methods(["GET"])
def movie_detail(request: HttpRequest, movie_id: int) -> JsonResponse:
    movie = get_object_or_404(Movie, id=movie_id)
    return JsonResponse({"movie": _serialize_movie(movie)})
