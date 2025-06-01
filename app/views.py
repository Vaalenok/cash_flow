from django.contrib import messages
from django.db.models import ProtectedError
from django.shortcuts import render, get_object_or_404, redirect

from .forms import CashFlowForm, TypeForm, CategoryForm, SubcategoryForm, StatusForm
from .models import CashFlow, Type, Status, Category, Subcategory


def custom_404(request, exception):
    return render(request, "app/404.html", status=404)


def cashflow_list(request):
    qs = CashFlow.objects.all()

    type_id = request.GET.get("type")
    status_id = request.GET.get("status")
    category_id = request.GET.get("category")
    subcategory_id = request.GET.get("subcategory")
    date_from = request.GET.get("date_from")
    date_to = request.GET.get("date_to")
    amount_min = request.GET.get("amount_min")
    amount_max = request.GET.get("amount_max")
    comment = request.GET.get("comment")

    if status_id:
        qs = qs.filter(status_id=status_id)

    if type_id:
        qs = qs.filter(category__category__type_id=type_id)

    if category_id:
        qs = qs.filter(category__category_id=category_id)

    if subcategory_id:
        qs = qs.filter(category_id=subcategory_id)

    if date_from:
        qs = qs.filter(date_of_create__gte=date_from)

    if date_to:
        qs = qs.filter(date_of_create__lte=date_to)

    if amount_min:
        qs = qs.filter(amount__gte=amount_min)

    if amount_max:
        qs = qs.filter(amount__lte=amount_max)

    if comment:
        qs = qs.filter(comment__icontains=comment)

    types = Type.objects.all()

    if type_id:
        categories = Category.objects.filter(type_id=type_id)
    else:
        categories = Category.objects.all()

    if category_id:
        subcategories = Subcategory.objects.filter(category_id=category_id).all()
    else:
        subcategories = Subcategory.objects.all()

    context = {
        "cashflows": qs,
        "types": types,
        "statuses": Status.objects.all(),
        "categories": categories,
        "subcategories": subcategories
    }

    return render(request, "app/cashflow_list.html", context)


def cashflow_create(request):
    if request.method == "POST":
        form = CashFlowForm(request.POST)

        if form.is_valid():
            form.save()
            return redirect("cashflow_list")
    else:
        form = CashFlowForm()

    return render(request, "app/cashflow_create-edit.html", {"form": form})


def cashflow_edit(request, pk=None):
    instance = get_object_or_404(CashFlow, pk=pk) if pk else None

    if request.method == "POST":
        action = request.POST.get("action")
        form = CashFlowForm(request.POST, instance=instance)

        match action:
            case "save":
                if form.is_valid():
                    form.save()

            case "delete":
                instance.delete()

        return redirect("cashflow_list")
    else:
        initial = {}

        if instance and instance.category:
            initial["category_filter"] = instance.category.category
            initial["type_filter"] = instance.category.category.type

        form = CashFlowForm(instance=instance, initial=initial)

    return render(request, "app/cashflow_create-edit.html", {"form": form, "object": instance})


def reference_edit(request):
    if request.method == "POST":
        action = request.POST.get("action")
        obj_id = request.POST.get("id")
        form = None

        try:
            match action:
                case "add_type":
                    form = TypeForm(request.POST)

                case "delete_type":
                    Type.objects.filter(id=obj_id).delete()

                case "add_category":
                    form = CategoryForm(request.POST)

                case "delete_category":
                    Category.objects.filter(id=obj_id).delete()

                case "add_subcategory":
                    form = SubcategoryForm(request.POST)

                case "delete_subcategory":
                    Subcategory.objects.filter(id=obj_id).delete()

                case "add_status":
                    form = StatusForm(request.POST)

                case "delete_status":
                    Status.objects.filter(id=obj_id).delete()
        except ProtectedError:
            messages.error(request, "Невозможно удалить: объект используется в других записях.")

        if form and form.is_valid():
            form.save()

        return redirect("reference_edit")

    context = {
        "types": Type.objects.all(),
        "categories": Category.objects.select_related("type"),
        "subcategories": Subcategory.objects.select_related("category__type"),
        "statuses": Status.objects.all(),

        "type_form": TypeForm(),
        "category_form": CategoryForm(),
        "subcategory_form": SubcategoryForm(),
        "status_form": StatusForm()
    }

    return render(request, "app/reference_edit.html", context)
