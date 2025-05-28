import datetime
from django.db import models


class Category(models.Model):
    name = models.CharField(max_length=100)


class Subcategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.PROTECT, related_name="subcategories")


class Type(models.Model):
    name = models.CharField(max_length=100)


class Status(models.Model):
    name = models.CharField(max_length=100)


class CashFlow(models.Model):
    date_of_create = models.DateField(default=datetime.date.today)
    status = models.ForeignKey(Status, on_delete=models.PROTECT, related_name="cash_flows")
    type = models.ForeignKey(Type, on_delete=models.PROTECT, related_name="cash_flows")
    category = models.ForeignKey(Subcategory, on_delete=models.PROTECT, related_name="cash_flows")
    amount = models.FloatField()
    comment = models.TextField(blank=True)
