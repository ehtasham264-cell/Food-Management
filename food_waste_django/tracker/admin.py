from django.contrib import admin
from .models import InventoryItem, SurplusItem, WasteEntry

admin.site.register(InventoryItem)
admin.site.register(WasteEntry)
admin.site.register(SurplusItem)
