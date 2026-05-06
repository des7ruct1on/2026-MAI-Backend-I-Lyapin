from django.http import JsonResponse
from django.shortcuts import render
from django.views.decorators.http import require_http_methods


@require_http_methods(["GET"])
def web_index(request):
    return render(request, "main/index.html", {})


@require_http_methods(["GET"])
def api_profile(request):
    return JsonResponse({"id": 1, "username": "demo", "email": "demo@example.com"})


@require_http_methods(["GET"])
def api_products(request):
    return JsonResponse(
        {
            "items": [
                {"id": 1, "title": "Product 1", "price": 100},
                {"id": 2, "title": "Product 2", "price": 200},
            ]
        }
    )


@require_http_methods(["GET"])
def api_category(request, category_id: int):
    return JsonResponse({"id": category_id, "title": f"Category {category_id}", "products": [1, 2]})


@require_http_methods(["POST"])
def api_favorites_add(request):
    return JsonResponse({"ok": True})
