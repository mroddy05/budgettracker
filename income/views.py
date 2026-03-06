from django.shortcuts import render
from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from django.core.paginator import Paginator
from .models import Income
from .forms import IncomeForm
from django.urls import reverse

def index(request):
    income_list = Income.objects.all().order_by('date')
    paginator = Paginator(income_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    return render(
        request, 
        "income_page.html",
        {
            "incomes" : page_obj,
        },
    )

def add_income(request):
    success = False
    added_expense = None

    if request.method == "POST":
        form = IncomeForm(request.POST)
        if form.is_valid():
            new_income = form.save()
            success = True
            added_income = new_income
            return redirect("income_page")

            
    else:
        form = IncomeForm()
    
    income_list = Income.objects.all().order_by('date')
    paginator = Paginator(income_list, 10)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "income_page.html", 
        {"form": form,
         "added_income": added_income,
         "success": success},
    )


def edit_income(request, income_id, page_number):
    pn = request.GET.get("page", page_number)
    print(f"[DBG] edit_income {income_id}, {page_number}, {pn} <<<")
    success = False

    if request.method == "POST":
        income = Income.objects.get(id=income_id)
        income_name = request.POST.get("income_name")
        amount = request.POST.get("amount")
        date = request.POST.get("date")
        frequency = request.POST.get("frequency")

        

        income.income_name = income_name
        income.amount = amount
        income.date = date
        income.frequency = frequency

        income.save()
        success = True


    income_list = Income.objects.all().order_by("date")
    paginator = Paginator(income_list, 10)
    page_number = request.POST.get(
        "page", request.GET.get("page", page_number)
    )
    page_obj = paginator.get_page(page_number)
    return render(
        request,
        "income_page.html",
        {
        "incomes": page_obj,
        "success": success,
        "updated_income_id": income_id,
    },
    )

def delete_income(request, income_id, page_number):
    print("[DBG] delete_income called for ID:", income_id)
    if request.method == "POST":
        expense = get_object_or_404(Income, id=income_id)
        expense.delete()

        return redirect("/income/?page={page_number}")

