from django.db import models

class Budget(models.Model):
    category = models.CharField(max_length=20)
    percentage = models.FloatField()
