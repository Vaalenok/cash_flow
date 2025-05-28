from django.urls import path
from . import views


urlpatterns = [
    path("", views.cashflow_list, name="cashflow_list"),
    # path("add/", views.cashflow_create, name="cashflow_add"),
    # path("edit/<int:pk>/", views.cashflow_edit, name="cashflow_edit"),
    # path("delete/<int:pk>/", views.cashflow_delete, name="cashflow_delete")
]
