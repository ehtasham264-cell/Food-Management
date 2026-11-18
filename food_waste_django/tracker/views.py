import json
from datetime import date

from django.http import JsonResponse
from django.shortcuts import get_object_or_404, render
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_http_methods

from .models import InventoryItem, SurplusItem, WasteEntry


def body(request):
    try:
        return json.loads(request.body or "{}")
    except json.JSONDecodeError:
        return {}


def bad(message):
    return JsonResponse({"error": message}, status=400)


def home(request):
    return render(request, "index.html")


@require_http_methods(["GET"])
def data(request):
    return JsonResponse({
        "inv": [
            {"id": i.id, "name": i.name, "qty": i.qty, "unit": i.unit,
             "cost": i.cost, "exp": i.expiry.isoformat()}
            for i in InventoryItem.objects.all()
        ],
        "waste": [
            {"date": w.date.isoformat(), "name": w.name, "qty": w.qty,
             "cost": w.cost, "reason": w.reason}
            for w in WasteEntry.objects.all()
        ],
        "surplus": [
            {"id": s.id, "dish": s.dish, "portions": s.portions, "action": s.action}
            for s in SurplusItem.objects.all()
        ],
    })


# CSRF is skipped to keep this student project simple. Turn it back on
# (send the csrftoken cookie in a header) before using this in production.
@csrf_exempt
@require_http_methods(["POST"])
def add_inventory(request):
    d = body(request)
    try:
        name = str(d["name"]).strip()
        qty = float(d["qty"])
        expiry = date.fromisoformat(d["exp"])
    except (KeyError, ValueError, TypeError):
        return bad("Enter a name, a quantity and a valid expiry date.")
    if not name or qty <= 0:
        return bad("Name is required and quantity must be above 0.")
    item = InventoryItem.objects.create(
        name=name, qty=qty, unit=d.get("unit", "kg"),
        cost=float(d.get("cost") or 0), expiry=expiry)
    return JsonResponse({"id": item.id}, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_inventory(request, pk):
    get_object_or_404(InventoryItem, pk=pk).delete()
    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["POST"])
def inventory_to_waste(request, pk):
    item = get_object_or_404(InventoryItem, pk=pk)
    WasteEntry.objects.create(
        name=item.name, qty=item.qty,
        cost=round(item.qty * item.cost), reason="Expired")
    item.delete()
    return JsonResponse({"ok": True})


@csrf_exempt
@require_http_methods(["POST"])
def add_waste(request):
    d = body(request)
    try:
        name = str(d["name"]).strip()
        qty = float(d["qty"])
    except (KeyError, ValueError, TypeError):
        return bad("Enter an item and a quantity.")
    if not name or qty <= 0:
        return bad("Item is required and quantity must be above 0.")
    WasteEntry.objects.create(
        name=name, qty=qty, cost=float(d.get("cost") or 0),
        reason=d.get("reason", "Expired"))
    return JsonResponse({"ok": True}, status=201)


@csrf_exempt
@require_http_methods(["POST"])
def add_surplus(request):
    d = body(request)
    try:
        dish = str(d["dish"]).strip()
        portions = int(d["portions"])
    except (KeyError, ValueError, TypeError):
        return bad("Enter a dish and the number of portions.")
    if not dish or portions <= 0:
        return bad("Dish is required and portions must be above 0.")
    SurplusItem.objects.create(dish=dish, portions=portions, action=d.get("action", "Discount sale"))
    return JsonResponse({"ok": True}, status=201)


@csrf_exempt
@require_http_methods(["DELETE"])
def delete_surplus(request, pk):
    get_object_or_404(SurplusItem, pk=pk).delete()
    return JsonResponse({"ok": True})
