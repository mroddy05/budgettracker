from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='income_page'),
    path('add/', views.add_income, name='add_income'),
    path('edit_income/<int:income_id>/<int:page_number>/', 
                views.edit_income, name='edit_income'),
    path('delete_income/<int:income_id>/<int:page_number>/', 
                views.delete_income, name='delete_income'),
    
]