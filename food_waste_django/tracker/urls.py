from django.urls import path
from . import views

urlpatterns = [
    path("", views.home, name="home"),
    path("api/data/", views.data),
    path("api/inventory/", views.add_inventory),
    path("api/inventory/<int:pk>/", views.delete_inventory),
    path("api/inventory/<int:pk>/waste/", views.inventory_to_waste),
    path("api/waste/", views.add_waste),
    path("api/surplus/", views.add_surplus),
    path("api/surplus/<int:pk>/", views.delete_surplus),
]
