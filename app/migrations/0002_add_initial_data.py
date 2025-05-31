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
    types = {
        "Пополнение": {
            "Инфраструктура": ["VPS", "Proxy"]
        },
        "Списание": {
            "Маркетинг": ["Farpost", "Avito"]
        }
    }

    for type_name, _category in types.items():
        new_type = _type.objects.create(name=type_name)

        for category_name, sub_names in _category.items():
            new_category = category.objects.create(name=category_name, type=new_type)

            for sub_name in sub_names:
                subcategory.objects.create(name=sub_name, category=new_category)


class Migration(migrations.Migration):

    dependencies = [
        ('app', '0001_initial_migration'),
    ]

    operations = [
        migrations.RunPython(add_initial_data)
    ]
