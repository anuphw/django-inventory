from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from django.views.generic.edit import FormView
from django.views.generic import TemplateView
from .models import *
# from .forms import ProjectForm, FileUploadForm
from .forms import (MaterialQtyForm, PurchaseForm, MaterialFormSet, 
MaterialQtyTransferForm, TransferForm, TransferFormSet)
from django.urls import reverse_lazy


class CategoryCreateAndListView(CreateView):
    model = Category
    template_name = 'materials/category_create.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_list'] = self.model.objects.all()
        context['form_name'] = 'New Category'
        context['list_name'] = 'Categories'
        context['update'] = False
        return context
    
    def get_success_url(self):
        return reverse('materials:category')

class CategoryUpdateView(UpdateView):
    model = Category
    template_name = 'materials/category_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['category_list'] = self.model.objects.all()
        context['form_name'] = 'New Category'
        context['list_name'] = 'Categories'
        context['update'] = True
        return context
    
    def get_success_url(self):
        return reverse('materials:category')

class CategoryDeleteView(DeleteView):
    model = Category
    success_url = reverse_lazy('materials:category')

    def get(self, request, *args, **kwargs):
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:category'))   

# Brands
class BrandCreateAndListView(CreateView):
    model = Brand
    template_name = 'materials/brand_create.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['brand_list'] = self.model.objects.all()
        context['form_name'] = 'New Brand'
        context['list_name'] = 'Brands'
        context['update'] = False
        return context
    
    def get_success_url(self):
        return reverse('materials:brand')

class BrandUpdateView(UpdateView):
    model = Brand
    template_name = 'materials/brand_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['brand_list'] = self.model.objects.all()
        context['form_name'] = 'Update Brand'
        context['list_name'] = 'Brands'
        context['update'] = True
        return context
    
    def get_success_url(self):
        return reverse('materials:brand')

class BrandDeleteView(DeleteView):
    model = Brand
    success_url = reverse_lazy('materials:brand')

    def get(self, request, *args, **kwargs):
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:brand'))   

# Units
class UnitCreateAndListView(CreateView):
    model = Units
    template_name = 'materials/unit_create.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['unit_list'] = self.model.objects.all()
        context['form_name'] = 'New Unit'
        context['list_name'] = 'Units'
        context['update'] = False
        return context
    
    def get_success_url(self):
        return reverse('materials:unit')

class UnitUpdateView(UpdateView):
    model = Units
    template_name = 'materials/unit_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['unit_list'] = self.model.objects.all()
        context['form_name'] = 'Update Unit'
        context['list_name'] = 'Units'
        context['update'] = True
        return context
    
    def get_success_url(self):
        return reverse('materials:unit')

class UnitDeleteView(DeleteView):
    model = Units
    success_url = reverse_lazy('materials:unit')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:unit'))   

class CategoryAddPopup(CreateView):
    model = Category
    template_name = 'materials/category_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

class BrandAddPopup(CreateView):
    model = Brand
    template_name = 'materials/brand_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_brand");</script>' % (instance.pk, instance))

class UnitsAddPopup(CreateView):
    model = Units
    template_name = 'materials/unit_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_units");</script>' % (instance.pk, instance))


class MaterialAddPopup(CreateView):
    model = Material
    template_name = 'materials/material_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_material");</script>' % (instance.pk, instance))


class MaterialCreateView(CreateView):
    model = Material
    template_name = 'materials/material_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('materials:material_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = False
        context['form_name'] = 'Create Material'
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)

class MaterialUpdateView(UpdateView):
    model = Material
    template_name = 'materials/material_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('materials:material_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = True
        context['form_name'] = 'Update Material'
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)

class MaterialDeleteView(DeleteView):
    model = Material
    success_url = reverse_lazy('materials:material_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:material_list'))   

class MaterialListView(ListView):
    model = Material
    template_name = 'materials/material_list.html'
    fields = '__all__'


# City

class CityCreateAndListView(CreateView):
    model = City
    template_name = 'materials/city_create.html'
    fields = '__all__'
    
    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['city_list'] = self.model.objects.all()
        context['form_name'] = 'New City'
        context['list_name'] = 'City'
        context['update'] = False
        return context
    
    def get_success_url(self):
        return reverse('materials:city')

class CityUpdateView(UpdateView):
    model = City
    template_name = 'materials/city_create.html'
    fields = '__all__'

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['city_list'] = self.model.objects.all()
        context['form_name'] = 'New City'
        context['list_name'] = 'City'
        context['update'] = True
        return context
    
    def get_success_url(self):
        return reverse('materials:city')

class CityDeleteView(DeleteView):
    model = City
    success_url = reverse_lazy('materials:city')

    def get(self, request, *args, **kwargs):
        #self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:city'))   

class CityAddPopup(CreateView):
    model = City
    template_name = 'materials/city_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_city");</script>' % (instance.pk, instance))

# Warehouses
class WarehouseAddPopup(CreateView):
    model = Warehouse
    template_name = 'materials/warehouse_create.html'
    fields = '__all__'

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_warehouse");</script>' % (instance.pk, instance))


class WarehouseCreateView(CreateView):
    model = Warehouse
    template_name = 'materials/warehouse_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('materials:warehouse_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = False
        context['form_name'] = 'Create Warehouse'
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)

class WarehouseUpdateView(UpdateView):
    model = Warehouse
    template_name = 'materials/warehouse_create.html'
    fields = '__all__'

    def get_success_url(self):
        return reverse('materials:warehouse_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = True
        context['form_name'] = 'Update Warehouse'
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)

class WarehouseDeleteView(DeleteView):
    model = Warehouse
    success_url = reverse_lazy('materials:warehouse_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:warehouse_list'))   

class WarehouseListView(ListView):
    model = Warehouse
    template_name = 'materials/warehouse_list.html'
    fields = '__all__'


# Inventory

class InventoryCreateView(CreateView):
    model = Inventory
    template_name = 'materials/inventory_create.html'
    fields = ['material','warehouse','low_level']

    def get_success_url(self):
        return reverse('materials:inventory_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = False
        context['form_name'] = 'Create Inventory'
        return context
        
    def form_valid(self, form):
        return super().form_valid(form)

class InventoryUpdateView(UpdateView):
    model = Inventory
    template_name = 'materials/inventory_create.html'
    fields = ['material','warehouse','low_level','quantity']

    def get_success_url(self):
        return reverse('materials:inventory_list')

    def get_context_data(self, **kwargs):
        context =  super().get_context_data(**kwargs)
        context['update'] = True
        context['form_name'] = 'Update Inventory'
        return context
        
    def form_valid(self, form):
        object = self.get_object()
        pre_qty = object.quantity
        post_qty = form.instance.quantity
        user = self.request.user
        adj = InventoryAdjustment(inventory = object,
        adjustment_amount=post_qty-pre_qty,
        user=user)
        adj.save()
        return super().form_valid(form)

class InventoryDeleteView(DeleteView):
    model = Inventory
    success_url = reverse_lazy('materials:inventory_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:inventory_list'))   

class InventoryListView(ListView):
    model = Inventory
    template_name = 'materials/inventory_list.html'
    fields = '__all__'

# Inventory Adjustment
class InventoryAdjListView(ListView):
    model = InventoryAdjustment
    template_name = 'materials/inventory_adj_list.html'
    fields = '__all__'

# Purchases

class PurchasesListView(ListView):
    model = Purchase
    template_name = '/materials/purchase_list.html'
    fields = '__all__'


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = '/materials/purchase_detail.html'
    fields = '__all__'

class PurchaseCreateView(CreateView):
    model = Purchase
    forms = PurchaseForm
    template_name = 'materials/purchase_create.html'
    fields = ['date','description','supplier','warehouse','project']

    def get_success_url(self):
        return reverse('materials:purchase_detail',kwargs={pk:self.id})

    def get_context_data(self, **kwargs):
        context = super(PurchaseCreateView, self).get_context_data(**kwargs)
        formset = MaterialFormSet(queryset=Material.objects.none())
        context['formset'] = formset
        return context
    
    def post(self, request, *args, **kwargs):
        materials = MaterialFormSet(request.POST)
        purchase = PurchaseForm(request.POST)
        if materials.is_valid() and purchase.is_valid():
            return self.form_valid(materials,purchase)
    
    def form_valid(self, materials,purchase):
        user = self.request.user
        parent = purchase.save(commit = False)
        parent.user = user
        parent.save()
        for material in materials:
            child = material.save(commit=False)
            child.purchase = parent
            print('*'*20)
            print(child)
            child.save()
        return HttpResponseRedirect(reverse('materials:purchase_list'))

class MaterialTransferCreateView(CreateView):
    model = MaterialTransfer
    forms = TransferForm
    template_name = 'materials/transfer_create.html'
    fields = ['date','source','destination','project']

    def get_success_url(self):
        return reverse('materials:transfer_list')

    def get_context_data(self, **kwargs):
        context = super(MaterialTransferCreateView, self).get_context_data(**kwargs)
        formset = TransferFormSet(queryset=Material.objects.none())
        context['formset'] = formset
        return context
    
    def post(self, request, *args, **kwargs):
        materials = TransferFormSet(request.POST)
        transfer = TransferForm(request.POST)
        if materials.is_valid() and transfer.is_valid():
            return self.form_valid(materials,transfer)
    
    def form_valid(self, materials,transfer):
        user = self.request.user
        parent = transfer.save(commit = False)
        parent.user = user
        parent.save()
        for material in materials:
            child = material.save(commit=False)
            child.purchase = parent
            print('*'*20)
            print(child)
            child.save()
        return HttpResponseRedirect(reverse('materials:transfer_list'))
