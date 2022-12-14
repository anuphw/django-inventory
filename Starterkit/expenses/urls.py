from django.urls import path
from .views import *
from django.conf import settings
from django.conf.urls.static import static

app_name = 'expenses'

urlpatterns = [
    path('expcat/',ExpCategoryCreateAndListView.as_view(),name='expcategory'),
    path('expcat/<int:pk>',ExpCategoryUpdateView.as_view(),name='expcategory_update'),
    path('expcat/<int:pk>/delete',ExpCategoryDeleteView.as_view(),name='expcategory_delete'),
    path('create/',ExpenseCreateSimpleView.as_view(),name='expense_create'),
    path('',ExpenseListView.as_view(),name="expense_list"),
    path('<int:pk>',ExpenseDetailView.as_view(),name='expense_detail'),
    path('<int:pk>/delete',ExpenseDeleteView.as_view(),name='expense_delete'),
]