from django.shortcuts import render, get_object_or_404, redirect
from django.core.paginator import Paginator
from .models import Expense
from .forms import ExpenseForm
from budget.models import Budget
from income.models import Income
from datetime import date
from django.db.models import Sum


def balanced_budget():
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


def budget_overview_values():
    today = date.today()
    curr_month = today.month
    curr_year = today.year

    total_monthly_income = Income.objects.filter(
        date__month=curr_month,
        date__year=curr_year
    ).aggregate(total=Sum('amount'))['total'] or 0  

    
    budget_values = Budget.objects.all()
    if not budget_values.exists():
        balanced_budget()
        budget_values = Budget.objects.all()

    budget_overview = {}
    for budget in budget_values:
        allowed = float(budget.percentage) * float(total_monthly_income)
        spent = Expense.objects.filter(
            expense_type=budget.category,
            date__month=curr_month,
            date__year=curr_year
        ).aggregate(total=Sum('amount'))['total'] or 0    


        budget_overview[budget.category] = {"allowed": allowed, "spent": spent}
    
    
    total_expenses = Expense.objects.filter(
        date__month=curr_month,
        date__year=curr_year
    ).aggregate(total=Sum('amount'))['total'] or 0

    return (budget_overview, total_monthly_income, total_expenses)


def month_logic():
    today = date.today()
    if today.month == 1:
        last_month = 12
        last_year = today.year - 1
    else:
        last_month = today.month - 1
        last_year = today.year

    lm_expenses = Expense.objects.filter(frequency = 'MONTHLY',
        date__month=last_month,
        date__year=last_year)
    for exp in lm_expenses:
        
        if_exists = Expense.objects.filter(
            expense_name=exp.expense_name,
            date__month=today.month,
            date__year=today.year,
            date__day=exp.date.day).exists()
        
        if not if_exists:
            Expense.objects.create(
                expense_name=exp.expense_name,
                expense_type=exp.expense_type,
                amount=exp.amount,
                date=today.replace(day=exp.date.day),
                frequency=exp.frequency
            )

def year_logic():
    today = date.today()
    last_year = today.year - 1

    ly_expenses = Expense.objects.filter(
        frequency='YEARLY',
        date__year=last_year,
        date__month=today.month
    )

    for exp in ly_expenses:
        if_exists = Expense.objects.filter(
            expense_name=exp.expense_name,
            date__year=today.year,
            date__month=exp.date.month,
            date__day=exp.date.day
        ).exists()

        if not if_exists:
            Expense.objects.create(
                expense_name=exp.expense_name,
                expense_type=exp.expense_type,
                amount=exp.amount,
                date=exp.date.replace(year=today.year),
                frequency=exp.frequency
            )

def index(request):
    month_logic()
    year_logic()
    budget_overview, total_monthly_income, total_expenses = budget_overview_values()  
    expense_list = Expense.objects.all().order_by('-date')
    paginator = Paginator(expense_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "expenses": page_obj,
            "expenseTypes": Expense.expenseTypes,
            "frequencyTypes": Expense.frequencyTypes,
            "budget_overview": budget_overview,
            "total_monthly_income": total_monthly_income,
            "total_expenses": total_expenses
        },
    )

def add_expense(request):
    success = False
    added_expense = None
    error_message = None

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():

            amount = form.cleaned_data['amount']
            if amount >= 0:
                new_expense = form.save()
                success = True
                added_expense = new_expense
            else:
                error_message = "Amount can't be less than 0"

            return render(
                request,
                "add_expense.html", 
                {"form": form,
                 "added_expense": added_expense,
                 "success": success,
                 'error_message': error_message
                 },
            )
    else:
        form = ExpenseForm()
    return render(
        request,
        "add_expense.html", 
        {"form": form,
         "added_expense": added_expense,
         "success": success,
         'error_message': error_message
         },
    )

def search_expense(request):
    page_number = request.GET.get("page", 1)
    expense_name = request.GET.get("expense_name", "").strip()
    expense_type = request.GET.get("expense_type", "").strip()
    amount = request.GET.get("amount", "").strip()
    date = request.GET.get("date", "").strip()
    frequency = request.GET.get("frequency", "").strip()

    if request.method == "POST":
        page_number = request.POST.get("page", 1)
        expense_name = request.POST.get("expense_name", "").strip()
        expense_type = request.POST.get("expense_type", "").strip()
        amount = request.POST.get("amount", "").strip()
        date = request.POST.get("date", "").strip()
        frequency = request.POST.get("frequency", "").strip()

        page_number = 1

    expenses = Expense.objects.all().order_by("-date")

    if expense_name:
        expenses = expenses.filter(expense_name__icontains=expense_name)

    if expense_type:
        expenses = expenses.filter(expense_type__icontains=expense_type)

    if frequency:
        expenses = expenses.filter(frequency__icontains=frequency)

    if amount:
        expenses = expenses.filter(amount=amount)

    if date:
        expenses = expenses.filter(date=date)

    expenses = expenses.order_by("-date")
    
    paginator = Paginator(expenses, 10)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "search_expense.html",
        {"expenses": page_obj,
         "expense_name_query": expense_name,
         "expense_type_query": expense_type,
         "amount_query": amount,
         "date_query": date,
         "frequency_query": frequency,
         "type_choices": Expense.expenseTypes,
         "frequency_choices": Expense.frequencyTypes},
    )

def edit_expense(request, expense_id, page_number):
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_expense {expense_id}, {page_number}, {pn} <<<")
    success = False
    error_message = ""

    if request.method == "POST":
        expense = Expense.objects.get(id=expense_id)
        expense_name = request.POST.get("expense_name")
        expense_type = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        frequency = request.POST.get("frequency")

        if not amount:
            error_message = "Amount is required"
        elif float(amount) >= 0:
            expense.expense_name = expense_name
            expense.expense_type = expense_type
            expense.amount = amount
            expense.date = date
            expense.frequency = frequency
            expense.save()
            success = True
        else:
            error_message = "Amount can't be negative"

    expense_list = Expense.objects.all().order_by("-date")
    paginator = Paginator(expense_list, 10)
    page_number = request.POST.get(
        "page", request.GET.get("page", page_number)
    )
    page_obj = paginator.get_page(page_number)
    budget_overview, total_monthly_income, total_expenses = budget_overview_values()
    return render(
        request,
        "index.html",
        {
        "budget_overview": budget_overview,
        "expenseTypes": Expense.expenseTypes,
        "frequencyTypes": Expense.frequencyTypes,
        "total_monthly_income": total_monthly_income,
        "total_expenses": total_expenses,
        "expenses": page_obj,
        "success": success,
        "updated_expense_id": expense_id,
        "error_message": error_message,
    },
    )

def delete_expense(request, expense_id, page_number):
    print("[DBG] delete_expense called for ID:", expense_id)
    if request.method == "POST":
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()

        return redirect(f"/?page={page_number}")

