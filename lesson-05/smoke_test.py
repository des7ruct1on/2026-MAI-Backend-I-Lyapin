import os
import sys


def main() -> None:
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    django_project_root = os.path.join(repo_root, "project")
    sys.path.insert(0, django_project_root)

    os.environ.setdefault("USE_SQLITE", "1")
    os.environ.setdefault("DJANGO_SETTINGS_MODULE", "project.settings")

    import django  # noqa: E402

    django.setup()

    from django.test import Client  # noqa: E402
    from movies.models import Genre, Movie  # noqa: E402

    Genre.objects.all().delete()
    Movie.objects.all().delete()

    thriller = Genre.objects.create(name="Thriller")
    Movie.objects.create(
        title="Silence of the Lambs",
        description="Cult classic thriller",
        year=1991,
        genre=thriller,
    )
    Movie.objects.create(
        title="Silence",
        description="Description without keyword",
        year=2001,
        genre=thriller,
    )
    Movie.objects.create(
        title="Another movie",
        description="silence of doctor evans",
        year=2020,
        genre=thriller,
    )

    c = Client()

    resp = c.get("/api/search/", {"q": "silence"})
    assert resp.status_code == 200, resp.status_code
    assert len(resp.json()["movies"]) == 3, resp.json()

    resp = c.get("/api/movies/")
    assert resp.status_code == 200, resp.status_code

    resp = c.post(
        "/api/movies/create",
        data=f'{{"title":"X","description":"Y","year":2026,"genre_id":{thriller.id}}}',
        content_type="application/json",
    )
    assert resp.status_code == 201, resp.content

    print("OK")


if __name__ == "__main__":
    main()

