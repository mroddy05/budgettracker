from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Expense
from .forms import ExpenseForm

def index(request):
    expense_list = Expense.objects.all().order_by('date')
    paginator = Paginator(expense_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request,
        "index.html",
        {
            "expenses": page_obj,
        },
    )

def add_expense(request):
    success = False
    added_expense = None

    if request.method == "POST":
        form = ExpenseForm(request.POST)
        if form.is_valid():
            new_expense = form.save()
            success = True
            added_expense = new_expense

            return render(
                request,
                "add_expense.html", 
                {"form": form,
                 "added_expense": added_expense,
                 "success": success},
            )
    else:
        form = ExpenseForm()
    return render(
        request,
        "add_expense.html", 
        {"form": form,
         "added_expense": added_expense,
         "success": success},
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

    expenses = Expense.objects.all().order_by("date")

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

    expenses = expenses.order_by("date")
    
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
         "frequency_query": frequency},
    )

def edit_expense(request, expense_id, page_number):
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_expense {expense_id}, {page_number}, {pn} <<<")
    success = False

    if request.method == "POST":
        expense = Expense.objects.get(id=expense_id)
        expense_name = request.POST.get("expense_name")
        expense_type = request.POST.get("expense_type")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        description = request.POST.get("description")
        frequency = request.POST.get("frequency")

        

        expense.expense_name = expense_name
        expense.expense_type = expense_type
        expense.amount = amount
        expense.date = date
        expense.description = description
        expense.frequency = frequency

        expense.save()
        success = True

    expense_list = Expense.objects.all().order_by("date")
    paginator = Paginator(expense_list, 10)
    page_number = request.POST.get(
        "page", request.GET.get("page", page_number)
    )
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "index.html",
        {
        "expenses": page_obj,
        "success": success,
        "updated_expense_id": expense_id,
    },
    )

def delete_expense(request, expense_id, page_number):
    print("[DBG] delete_expense called for ID:", expense_id)
    if request.method == "POST":
        expense = get_object_or_404(Expense, id=expense_id)
        expense.delete()

        return redirect(f"/?page={page_number}")

