from django.shortcuts import render

from .models import CashFlow, Type, Status, Category


def cashflow_list(request):
    qs = CashFlow.objects.all()

    type_id = request.GET.get("type")
    status_id = request.GET.get("status")
    category_id = request.GET.get("category")
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
        qs = qs.filter(category_id=category_id)

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

    context = {
        "cashflows": qs,
        "types": Type.objects.all(),
        "statuses": Status.objects.all(),
        "categories": Category.objects.all(),
    }

    return render(request, "app/cashflow_list.html", context)
