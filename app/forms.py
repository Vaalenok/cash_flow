from django import forms
from .models import CashFlow, Subcategory, Category, Type, Status


class TypeForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Type
        fields = ["name"]


class CategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    type = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Category
        fields = ["name", "type"]


class SubcategoryForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    category = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        widget=forms.Select(attrs={"class": "form-control"})
    )

    class Meta:
        model = Subcategory
        fields = ["name", "category"]


class StatusForm(forms.ModelForm):
    name = forms.CharField(
        max_length=100,
        widget=forms.TextInput(attrs={"class": "form-control"})
    )

    class Meta:
        model = Status
        fields = ["name"]


class CashFlowForm(forms.ModelForm):
    type_filter = forms.ModelChoiceField(
        queryset=Type.objects.all(),
        required=True,
        label="Тип",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit();"})
    )

    category_filter = forms.ModelChoiceField(
        queryset=Category.objects.all(),
        required=True,
        label="Категория",
        widget=forms.Select(attrs={"class": "form-select", "onchange": "this.form.submit();"})
    )

    class Meta:
        model = CashFlow
        fields = ["date_of_create", "status", "category", "amount", "comment"]
        widgets = {
            "date_of_create": forms.DateInput(attrs={"type": "date", "class": "form-control"}),
            "comment": forms.Textarea(attrs={"rows": 3, "class": "form-control"}),
            "amount": forms.NumberInput(attrs={"class": "form-control"}),
            "status": forms.Select(attrs={"class": "form-select"}),
            "category": forms.Select(attrs={"class": "form-select"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        data = args[0] if args and isinstance(args[0], dict) else {}
        initial = kwargs.get("initial", {})

        if not self.data.get("type") and self.data.get("type_filter"):
            self.data = self.data.copy()
            self.data["type"] = self.data.get("type_filter")

        selected_type_id = None
        selected_category_id = None

        if data and data.get("type_filter"):
            try:
                selected_type_id = int(data.get("type_filter"))
            except (ValueError, TypeError):
                selected_type_id = None
        elif initial.get("type_filter"):
            selected_type_id = initial.get("type_filter")

        if selected_type_id and data.get("category_filter"):
            try:
                selected_category_id = int(data.get("category_filter"))
            except (ValueError, TypeError):
                selected_category_id = None
        elif initial.get("category_filter"):
            selected_category_id = initial.get("category_filter")

        self.fields["type_filter"].queryset = Type.objects.all()

        if selected_category_id:
            self.fields["category"].queryset = Subcategory.objects.filter(category_id=selected_category_id)
        else:
            self.fields["category"].queryset = Subcategory.objects.none()

        if selected_type_id:
            self.fields["category_filter"].queryset = Category.objects.filter(type_id=selected_type_id)
        else:
            self.fields["category_filter"].queryset = Category.objects.none()
