from django import forms
from .models import Budget

class BudgetForm(forms.Form):
    food = forms.FloatField(label="Food (%)")
    travel = forms.FloatField(label="Travel (%)")
    housing = forms.FloatField(label="Housing (%)")
    utilities = forms.FloatField(label="Utilities (%)")
    health = forms.FloatField(label="Health (%)")
    education = forms.FloatField(label="Education (%)")
    misc = forms.FloatField(label="Misc (%)")