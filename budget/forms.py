from django import forms
from .models import Budget

class BudgetForm(forms.Form):
    food = forms.FloatField(label="Food (%)", min_value=0, max_value=100)
    travel = forms.FloatField(label="Travel (%)", min_value=0, max_value=100)
    housing = forms.FloatField(label="Housing (%)", min_value=0, max_value=100)
    utilities = forms.FloatField(label="Utilities (%)", min_value=0, max_value=100)
    health = forms.FloatField(label="Health (%)", min_value=0, max_value=100)
    education = forms.FloatField(label="Education (%)", min_value=0, max_value=100)
    misc = forms.FloatField(label="Misc (%)", min_value=0, max_value=100)