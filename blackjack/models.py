from django.db import models


# Create your models here.
class Result(models.Model):
    name = models.CharField(max_length=30)
    average_profit = models.DecimalField(decimal_places=2, max_digits=10)

