from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='choose_budget'),
    path('balanced/', views.balanced_budget, name='balanced_budget'),
    path('conservative/', views.conservative_budget, name='conservative_budget'),
    path('student/', views.student_budget, name='student_budget'),
    path('high_living/', views.high_living_budget, name='high_living_budget'),
    path('custom/', views.custom_budget, name='custom_budget'),
]