from django import forms
from .models import CashFlow, Subcategory, Category


class CashFlowForm(forms.ModelForm):
    category_filter = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=False,
        label="Категория",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit();"})
    )

    class Meta:
        model = CashFlow
        fields = ["date_of_create", "status", "type", "category", "amount", "comment"]
        widgets = {
            "date_of_create": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "type": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = args[0] if args else None
        initial = kwargs.get('initial', {})

        selected_category_id = None

        if data and data.get("category_filter"):
            try:
                selected_category_id = int(data.get("category_filter"))
            except (ValueError, TypeError):
                selected_category_id = None
        elif initial.get("category_filter"):
            selected_category_id = initial.get("category_filter")

        if selected_category_id:
            self.fields["category"].queryset = Subcategory.objects.filter(category_id=selected_category_id)
        else:
            self.fields["category"].queryset = Subcategory.objects.none()
