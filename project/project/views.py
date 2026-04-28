from django.http import HttpResponse


def main_view(request):
    return HttpResponse(
        "<h1>Web</h1>"
        "<p>Это заглушка для location <code>/web/</code>.</p>"
        "<ul>"
        "<li><a href='/api/profile/'>/api/profile/</a></li>"
        "<li><a href='/api/movies/'>/api/movies/</a></li>"
        "<li><a href='/api/categories/1/'>/api/categories/1/</a></li>"
        "</ul>"
    )

