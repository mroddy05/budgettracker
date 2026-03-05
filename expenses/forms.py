from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_name', 'expense_type', 'amount', 'date', 'description', 'frequency']
        # Apply CSS styles
        widgets = {
            'expense_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter name of expense',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                },
                format='%Y-%m-%d'),
            'description': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter description of expense',
                }),
        }