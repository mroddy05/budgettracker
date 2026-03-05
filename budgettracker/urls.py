"""
URL configuration for budgettracker project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from expenses.views import add_expense
from expenses.views import delete_expense
from expenses.views import edit_expense
from expenses.views import search_expense
from expenses.views import index


urlpatterns = [
    # path('admin/', admin.site.urls),
    path('', index, name="index"),
    path('add/', add_expense, name="add_expense"),
    path('search/', search_expense, name='search_expense'),
    path('edit_expense/<int:expense_id>/<int:page_number>/',
          edit_expense, name='edit_expense'),
    path('delete_expense/<int:expense_id>/<int:page_number>/',
          delete_expense, name="delete_expense"),
]
