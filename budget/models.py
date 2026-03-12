from django.db import models
from django.core.validators import MinValueValidator, MaxValueValidator

class Budget(models.Model):
    category = models.CharField(max_length=20)
    percentage = models.FloatField(validators=[MinValueValidator(0), MaxValueValidator(100)])
