from django.shortcuts import render, redirect
from .models import Budget
from .forms import BudgetForm


def index(request):
    budget_list = Budget.objects.all()

    for budget in budget_list:
        budget.percentage = int(budget.percentage * 100)
        

    return render(
        request, 
        "choose_budget.html",
        {
            "budgets" : budget_list
        }
    )

def balanced_budget(request):
    if request.method == "POST":
        Budget.objects.all().delete()

        budgets = {
                "FOOD": 0.15,
                "TRAVEL": 0.10,
                "HOUSING": 0.30,
                "UTILITIES": 0.10,
                "HEALTH": 0.10,
                "EDUCATION": 0.10,
                "MISC": 0.15
            }
        
        for category, percent in budgets.items():
            Budget.objects.create(category=category, percentage=percent)
        

        return redirect("choose_budget")

def conservative_budget(request):
    if request.method == "POST":
        Budget.objects.all().delete()

        budgets = {
                "FOOD": 0.15,
                "TRAVEL": 0.05,
                "HOUSING": 0.25,
                "UTILITIES": 0.10,
                "HEALTH": 0.10,
                "EDUCATION": 0.10,
                "MISC": 0.25
            }
        
        for category, percent in budgets.items():
            Budget.objects.create(category=category, percentage=percent)
        

        return redirect("choose_budget")

def student_budget(request):
    if request.method == "POST":
        Budget.objects.all().delete()

        budgets = {
                "FOOD": 0.10,
                "TRAVEL": 0.05,
                "HOUSING": 0.35,
                "UTILITIES": 0.15,
                "HEALTH": 0.05,
                "EDUCATION": 0.25,
                "MISC": 0.05
            }
        
        for category, percent in budgets.items():
            Budget.objects.create(category=category, percentage=percent)
        

        return redirect("choose_budget")

def high_living_budget(request):
    if request.method == "POST":
        Budget.objects.all().delete()

        budgets = {
                "FOOD": 0.15,
                "TRAVEL": 0.10,
                "HOUSING": 0.40,
                "UTILITIES": 0.10,
                "HEALTH": 0.10,
                "EDUCATION": 0.05,
                "MISC": 0.10
            }
        
        for category, percent in budgets.items():
            Budget.objects.create(category=category, percentage=percent)
        

        return redirect("choose_budget")

def custom_budget(request):
    error_message = "Percentages must add to 100%"

    budget_list = Budget.objects.all()
    for budget in budget_list:
        budget.display_percent = int(budget.percentage * 100)

    if request.method == "POST":
        form = BudgetForm(request.POST)

        if form.is_valid():

            total = sum(form.cleaned_data.values())

            if total != 100:
                return render(
                    request,
                    "custom_budget.html",
                    {
                        "form": form,
                        "error_message": error_message
                    }
                )

            Budget.objects.all().delete()

            for category, percent in form.cleaned_data.items():
                Budget.objects.create(
                    category=category.upper(),
                    percentage=percent / 100
                )
            
            return redirect("choose_budget")
        
    else:
        form = BudgetForm()

    return render(request, 'custom_budget.html', {'form': form})
