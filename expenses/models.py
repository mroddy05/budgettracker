from django.db import models

class Expense(models.Model):
    expenseTypes = [
        ('FOOD', 'Food'),
        ('TRAVEL', 'Travel'),
        ('HOUSING', 'Housing'),
        ('UTILITIES', 'Utilities'),
        ('HEALTH', 'Health'),
        ('EDUCATION', 'Education'),
        ('MISC', 'Miscellaneous'),
    ]
    frequencyTypes = [
        ("ONE", "One-Time"),
        ('MONTHLY', 'Monthly'),
        ('YEARLY', 'Yearly'),
    ]

    expense_name = models.CharField(max_length=100)
    expense_type = models.CharField(max_length=20, choices=expenseTypes)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()
    description = models.TextField(blank=True, null=True)
    frequency = models.CharField(max_length=10, choices=frequencyTypes)