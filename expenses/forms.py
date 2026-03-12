from django import forms
from .models import Expense

class ExpenseForm(forms.ModelForm):
    class Meta:
        model = Expense
        fields = ['expense_name', 'expense_type', 'amount', 'date', 'frequency']
        # Apply CSS styles
        widgets = {
            'expense_name': forms.TextInput(attrs={
                'class': 'form-control', 
                'placeholder': 'Enter name of expense',
            }),
            'amount': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Enter amount',
                'min': '0',
                }),
            'date': forms.DateInput(attrs={
                'class': 'form-control',
                'type': 'date',
                },
                format='%Y-%m-%d'),
        }


    # def clean_amount(self):
    #     amount = self.cleaned_data.get('amount')
    #     if  amount < 0:
    #         raise forms.ValidationError("Amount can't be negative")
    #     return amount