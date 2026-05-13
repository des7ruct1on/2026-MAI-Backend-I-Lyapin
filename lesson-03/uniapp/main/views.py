import json

from django.db.models import Q
from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import Category, Product


def _product_dict(p: Product) -> dict:
    return {
        "id": p.id,
        "title": p.title,
        "description": p.description,
        "price": p.price,
        "category_id": p.category_id,
    }


@require_http_methods(["GET"])
def web_index(request):
    return render(request, "main/index.html", {})


@require_http_methods(["GET"])
def api_profile(request):
    return JsonResponse({"id": 1, "username": "demo", "email": "demo@example.com"})


@require_http_methods(["GET"])
def api_search(request):
    q = (request.GET.get("q") or "").strip()
    if not q:
        return JsonResponse({"error": "missing q"}, status=400)
    qs = Product.objects.filter(Q(title__icontains=q) | Q(description__icontains=q)).select_related(
        "category"
    )
    return JsonResponse({"items": [_product_dict(p) for p in qs]})


@require_http_methods(["GET"])
def api_products(request):
    qs = Product.objects.select_related("category").all().order_by("id")
    return JsonResponse({"items": [_product_dict(p) for p in qs]})


@require_http_methods(["POST"])
@csrf_exempt
def api_products_create(request):
    try:
        body = json.loads(request.body.decode() or "{}")
    except json.JSONDecodeError:
        return JsonResponse({"error": "invalid json"}, status=400)
    title = (body.get("title") or "").strip()
    if not title:
        return JsonResponse({"error": "title required"}, status=400)
    try:
        price = int(body.get("price", 0))
    except (TypeError, ValueError):
        return JsonResponse({"error": "price must be integer"}, status=400)
    if price < 0:
        return JsonResponse({"error": "price must be non-negative"}, status=400)
    category_id = body.get("category_id")
    category_title = body.get("category_title")
    if category_id is not None:
        try:
            category_id = int(category_id)
        except (TypeError, ValueError):
            return JsonResponse({"error": "category_id must be integer"}, status=400)
        try:
            category = Category.objects.get(pk=category_id)
        except Category.DoesNotExist:
            return JsonResponse({"error": "category not found", "category_id": category_id}, status=404)
    elif isinstance(category_title, str) and category_title.strip():
        category, _ = Category.objects.get_or_create(title=category_title.strip())
    else:
        return JsonResponse({"error": "send category_id or category_title"}, status=400)
    description = body.get("description")
    if description is None:
        description = ""
    if not isinstance(description, str):
        return JsonResponse({"error": "description must be string"}, status=400)
    p = Product.objects.create(
        title=title,
        description=description,
        price=price,
        category=category,
    )
    return JsonResponse(_product_dict(p), status=201)


@require_http_methods(["GET"])
def api_category(request, category_id: int):
    category = get_object_or_404(Category, pk=category_id)
    qs = category.products.all().order_by("id")
    return JsonResponse(
        {
            "id": category.id,
            "title": category.title,
            "products": [_product_dict(p) for p in qs],
        }
    )


@require_http_methods(["POST"])
@csrf_exempt
def api_favorites_add(request):
    return JsonResponse({"ok": True})
