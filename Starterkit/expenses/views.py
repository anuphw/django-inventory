from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from .models import *
from projects.models import Project, ProjectTimeline
from materials.models import Warehouse
from django.urls import reverse_lazy
# Create your views here.

class ExpCategoryCreateAndListView(CreateView):
    model = ExpenseCat
    template_name = 'expenses/category_create.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_list'] = self.model.objects.all()
        context['form_name'] = 'New Expense Category'
        context['list_name'] = 'Expense Categories'
        context['update'] = False
        return context
    
    def get_success_url(self):
        return reverse('expenses:expcategory')

class ExpCategoryUpdateView(UpdateView):
    model = ExpenseCat
    template_name = 'expenses/category_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_list'] = self.model.objects.all()
        context['form_name'] = 'Update Expense Category'
        context['list_name'] = 'Expense Categories'
        context['update'] = True
        return context
    
    def get_success_url(self):
        return reverse('expenses:expcategory')

class ExpCategoryDeleteView(DeleteView):
    model = ExpenseCat
    success_url = reverse_lazy('expenses:expcategory')

    def get(self, request, *args, **kwargs):
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('expenses:expcategory'))   


class ExpenseListView(ListView):
    model = Expense
    template_name = 'expenses/expense_list.html'
    fields = '__all__'

class ExpenseDetailView(DetailView):
    model = Expense
    template_name = 'expenses/expense_detail.html'
    fields = '__all__'


class ExpenseCreateSimpleView(View):
    def get(self,request):
        context = {
            'warehouses' : Warehouse.objects.all(),
            'projects' : Project.objects.all(),
            'exp_categories' : ExpenseCat.objects.all(),
        }
        return render(request,'expenses/expense_create_simple.html',context)
    
    def post(self,request):
        p = request.POST
        user = request.user
        dt = p['date']
        category = ExpenseCat.objects.get(pk=p['category'])
        amount = p['amount']
        details = p['description']
        if 'warehouse' in p.keys():
            Expense(
                date = dt,
                user = user,
                category = category,
                amount = amount,
                details = details,
                warehouse = Warehouse.objects.get(pk=p['warehouse'])
            ).save()
        elif 'project' in p.keys():
            project = Project.objects.get(pk=p['project'])
            exp = Expense(
                date = dt,
                user = user,
                category = category,
                amount = amount,
                details = details,
                project = project,
            )
            exp.save()
            pt = ProjectTimeline(
                project = project,
                status = project.status,
                user = user,
                notes = f"Added Expense worth {amount} on {dt} for {details}"
            )
            pt.save()
        return self.get(request)
        
class ExpenseDeleteView(DeleteView):
    model = Expense
    success_url = reverse_lazy('expenses:expense_list')

    def get(self, request, *args, **kwargs):
        expsense = self.get_object()
        user = request.user
        if expsense.project:
            pt = ProjectTimeline(
                project = expense.project,
                status = expense.project.status,
                user = user,
                notes = f"Deleted Expense worth {expense.amount} on {expense.date} for {expense.details}"
            )
            pt.save()
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)
    
    def post(self, request, *args, **kwargs):
        expsense = self.get_object()
        user = request.user
        if expsense.project:
            pt = ProjectTimeline(
                project = expense.project,
                status = expense.project.status,
                user = user,
                notes = f"Deleted Expense worth {expense.amount} on {expense.date} for {expense.details}"
            )
            pt.save()
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse('expenses:expense_list'))   