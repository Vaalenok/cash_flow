from django.urls import path
from . import views


urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"),
    path("create/", views.cashflow_create, name="cashflow_create"),
    path("edit/<int:pk>/", views.cashflow_edit, name="cashflow_edit"),
    path('references/', views.reference_edit, name="reference_edit")
]
