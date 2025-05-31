from django.shortcuts import render, get_object_or_404, redirect

from .forms import CashFlowForm
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

    if type_id:
        qs = qs.filter(type_id=type_id)

    if status_id:
        qs = qs.filter(status_id=status_id)

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

    return render(request, "app/cashflow_create-edit.html",
                  {"form": form, "back_url": request.META.get("HTTP_REFERER", "/")})


def cashflow_edit(request, pk=None):
    instance = get_object_or_404(CashFlow, pk=pk) if pk else None

    if request.method == "POST":
        action = request.POST.get("action")
        form = CashFlowForm(request.POST, instance=instance)

        if action == "save":
            if form.is_valid():
                form.save()
                return redirect("cashflow_list")
        elif action == "delete":
            instance.delete()
            return redirect("cashflow_list")
    else:
        initial = {}

        if instance and instance.category:
            initial["category_filter"] = instance.category.category
            initial["type_filter"] = instance.category.category.type

        form = CashFlowForm(instance=instance, initial=initial)

    return render(request, "app/cashflow_create-edit.html",
                  {"form": form, "object": instance, "back_url": request.META.get("HTTP_REFERER", "/")})
