from django.db import migrations


def add_initial_data(apps, schema_editor):
    category = apps.get_model("app", "Category")
    subcategory = apps.get_model("app", "Subcategory")
    _type = apps.get_model("app", "Type")
    status = apps.get_model("app", "Status")

    # Статусы
    statuses = ["Бизнес", "Личное", "Налог"]
    for status_name in statuses:
        status.objects.create(name=status_name)

    # Типы
    types = ["Пополнение", "Списание"]
    for type_name in types:
        _type.objects.create(name=type_name)

    # Категории и подкатегории
    categories_with_subs = {
        "Инфраструктура": ["VPS", "Proxy"],
        "Маркетинг": ["Farpost", "Avito"],
    }

    for category_name, sub_names in categories_with_subs.items():
        new_category = category.objects.create(name=category_name)

        for sub_name in sub_names:
            subcategory.objects.create(name=sub_name, category=new_category)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial_migration'),
    ]

    operations = [
        migrations.RunPython(add_initial_data)
    ]
