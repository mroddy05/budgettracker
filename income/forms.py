from django import forms
from .models import Income

class IncomeForm(forms.ModelForm):
    class Meta:
        model = Income
        fields = ['income_name', 'amount', 'frequency', 'date']
        # Apply CSS styles
        widgets = {
            'income_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter name of income',
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
        }