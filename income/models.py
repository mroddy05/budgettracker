from django.db import models

class Income(models.Model):
    frequencyTypes = [
        ("ONE", "One-Time"),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    income_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    frequency = models.CharField(max_length=10, choices=frequencyTypes)
    
    