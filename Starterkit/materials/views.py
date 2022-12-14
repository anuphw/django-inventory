from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
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
    fields = ['name']
    
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
    fields = ['name']

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
    fields = ['name']
    
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
    fields = ['name']

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
    fields = ['name']
    
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
    fields = ['name']

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
    fields = ['name']

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_category");</script>' % (instance.pk, instance))

class BrandAddPopup(CreateView):
    model = Brand
    template_name = 'materials/brand_create.html'
    fields = ['name']

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_brand");</script>' % (instance.pk, instance))

class UnitsAddPopup(CreateView):
    model = Units
    template_name = 'materials/unit_create.html'
    fields = ['name']

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_units");</script>' % (instance.pk, instance))


class MaterialAddPopup(CreateView):
    model = Material
    template_name = 'materials/material_create.html'
    fields = ['name','code','category','brand','unit','image']

    def form_valid(self, form):
        instance = form.save()
        try:
            target_id = self.kwargs['target_id']
        except:
            target_id = 'id_material'
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#%s");</script>' % (instance.pk, instance, target_id))

class MaterialCreateView(CreateView):
    model = Material
    template_name = 'materials/material_create.html'
    fields = ['name','code','category','brand','unit','image']

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
    fields = ['name','code','category','brand','unit','image']

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
    fields = ['name','code','category','brand','unit','image']


# City

class CityCreateAndListView(CreateView):
    model = City
    template_name = 'materials/city_create.html'
    fields = ['name']
    
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
    fields = ['name']

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
    fields = ['name']

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_city");</script>' % (instance.pk, instance))

# Warehouses
class WarehouseAddPopup(CreateView):
    model = Warehouse
    template_name = 'materials/warehouse_create.html'
    fields = ['name','address','contact','city']

    def form_valid(self, form):
        instance = form.save()
        return HttpResponse('<script>window.opener.closePopup(window, "%s", "%s", "#id_warehouse");</script>' % (instance.pk, instance))


class WarehouseCreateView(CreateView):
    model = Warehouse
    template_name = 'materials/warehouse_create.html'
    fields = ['name','address','contact','city']

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
    fields = ['name','address','contact','city']

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
    fields = ['name','address','contact','city']


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
    fields = ['material','warehouse','low_level','quantity']

# Inventory Adjustment
class InventoryAdjListView(ListView):
    model = InventoryAdjustment
    template_name = 'materials/inventory_adj_list.html'
    fields = ['inventory','adjustment_amount']

# Purchases

class PurchasesListView(ListView):
    model = Purchase
    template_name = '/materials/purchase_list.html'
    fields = '__all__'


class PurchaseDetailView(DetailView):
    model = Purchase
    template_name = '/materials/purchase_detail.html'
    fields = ['date','description','supplier','warehouse','project']

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
        context['form_name'] = 'Add Purchase'
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


class PurchaseSimpleView(View):
    def get(self,request):
        context = {
            'suppliers': Client.objects.order_by('name').all(),
            'warehouses': Warehouse.objects.order_by('name').all(),
            'projects': Project.objects.order_by('title').all(),
            'materials': Material.objects.order_by('name').all()
        }
        return render(request,'materials/purchase_create_simple.html',context=context)
    
    def post(self,request):
        print(request.POST)
        p = request.POST
        user = self.request.user
        dt = p['date']
        desc = p['description']
        supplier = Client.objects.filter(pk=p['supplier']).first()
        project = None
        warehouse = None
        if 'warehouse' in p.keys():
            warehouse = Warehouse.objects.filter(pk=p['warehouse']).first()
        elif 'project' in p.keys():
            project = Project.objects.filter(pk=p['project']).first()
            
            
        purchase = Purchase(
            date = dt,
            description = desc,
            supplier = supplier,
            warehouse = warehouse,
            project = project,
            user = user
        )   
        purchase.save()

        for k in p.keys():
            if 'material_' in k:
                material = Material.objects.filter(pk=p[k]).first()
                qty = p['quantity_'+k[9:]]
                price = p['price_'+k[9:]]
                m = MaterialQty(
                    material = material,
                    quantity = qty,
                    price = price,
                    purchase = purchase
                ).save()



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
        print(materials)
        transfer = TransferForm(request.POST)
        if materials.is_valid() and transfer.is_valid():
            return self.form_valid(materials,transfer)
        else:
            return MaterialTransferCreateView()
    
    def form_valid(self, materials,transfer):
        user = self.request.user
        parent = transfer.save(commit = False)
        parent.user = user
        parent.save()
        
        for material in materials:
            
            print('child.name',material.cleaned_data)
            if material.cleaned_data:
                child = material.save(commit=False)
                child.transfer = parent
                print('*'*20)
                print(child.material,child.quantity)
                print('*'*20)
                child.save()
        return HttpResponseRedirect(reverse('materials:transfer_list'))


class TransferListView(ListView):
    model = MaterialTransfer
    template_name = 'materials/transfer_list.html'

class TransferDetailView(DetailView):
    model = MaterialTransfer
    template_name = 'materials/transfer_detail.html'

class TransferDeleteView(DeleteView):
    model = MaterialTransfer
    success_url = reverse_lazy('materials:transfer_list')

    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(reverse_lazy('materials:transfer_list'))   


class MaterialReturnView(View):
    def post(self,request):
        p = request.POST
        dt = p['date']
        user = request.user
        project = Project.objects.get(pk=p['project'])
        material = Material.objects.get(pk=p['material'])
        qty = p['quantity']
        warehouse = Warehouse.objects.get(pk=p['warehouse'])
        inventory = Inventory.objects.get_or_create(material = material, warehouse=warehouse)
        pre_qty = inventory.quantity
        inventory.update(quantity = pre_qty + qty)
        m_ret = MaterialReturn(project=project,inventory=inventory,quantity = qty,date=dt, user=user).save()
        return HttpResponse(project.get_absolute_url)