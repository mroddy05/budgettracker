from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Income
from .forms import IncomeForm
from django.urls import reverse
from datetime import date
from django.db.models import Sum

def find_total_income():
    today = date.today()
    curr_month = today.month
    curr_year = today.year
    total_income = Income.objects.filter(
        date__month=curr_month,
        date__year=curr_year
    ).aggregate(total=Sum('amount'))['total'] or 0
    return total_income

def index(request):
    income_list = Income.objects.all().order_by('-date')
    paginator = Paginator(income_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    total_income = find_total_income()

    return render(
        request, 
        "income_page.html",
        {
            "incomes" : page_obj,
            "frequencyTypes": Income.frequencyTypes,
            "total_income": total_income,
        },
    )

def add_income(request):
    success = False
    added_income = None
    total_income = find_total_income()
    error_message = None

    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():

            amount = form.cleaned_data['amount']
            if amount >= 0:
                new_income = form.save()
                success = True
                added_income = new_income
                return redirect("income_page")
            else:
                error_message = "Amount can't be less than 0"

            
    else:
        form = IncomeForm()
    
    income_list = Income.objects.all().order_by('-date')
    paginator = Paginator(income_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "income_page.html", 
        {"form": form,
         "added_income": added_income,
         "total_income": total_income,
         "success": success,
         "incomes": page_obj,
         "frequencyTypes": Income.frequencyTypes,
         'error_message': error_message},
    )


def edit_income(request, income_id, page_number):
    error_message = None
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_income {income_id}, {page_number}, {pn} <<<")
    success = False

    total_income = find_total_income()

    if request.method == "POST":
        income = Income.objects.get(id=income_id)
        income_name = request.POST.get("income_name")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        frequency = request.POST.get("frequency")

        if not amount:
            error_message = "Amount is required"
        elif float(amount) >= 0:
            income.income_name = income_name
            income.amount = amount
            income.date = date
            income.frequency = frequency

            income.save()
            success = True
        else:
            error_message = "Amount can't be negative"

    income_list = Income.objects.all().order_by("-date")
    paginator = Paginator(income_list, 10)
    page_number = request.POST.get(
        "page", request.GET.get("page", page_number)
    )
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "income_page.html",
        {
        "error_message": error_message,
        "total_income": total_income,
        "incomes": page_obj,
        "success": success,
        "updated_income_id": income_id,
        "frequencyTypes": Income.frequencyTypes,
    },
    )

def delete_income(request, income_id, page_number):
    print("[DBG] delete_income called for ID:", income_id)
    if request.method == "POST":
        expense = get_object_or_404(Income, id=income_id)
        expense.delete()

        return redirect("/income/?page={page_number}")

