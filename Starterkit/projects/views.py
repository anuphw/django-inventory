from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import *
from clients.models import *
from .forms import ProjectForm, FileUploadForm, ProductFormSet
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from materials.models import Warehouse, Material, Inventory, MaterialReturn


def isnum(x):
    try:
        _ = float(x)
        return True
    except:
        return False

class StatusView(View):
    def get(self,request):
        context = {'status':Status.objects.order_by('order').all()}
        return render(request,'projects/status.html',context=context)
    
    def post(self,request):
        ids = []
        for k in request.POST.keys():
            if 'order-' in k:
                ids.append(k[6:])
        for i in ids:
            order, status, prob = int(request.POST['order-'+i][1:]), request.POST['status-'+i], float(request.POST['prob-'+i])
            Status.objects.filter(pk=i).update(order=order,status=status,probability=prob)
            print(f"order: {order} # status: {status} # prob: {prob}")
        return HttpResponseRedirect(reverse('projects:status'))

class StatusCreateView(View):
    def post(self,request):
        status = request.POST['status_name']
        prob = request.POST['prob']
        order = int(Status.objects.order_by('-order').first().order+1)
        Status(status= status, order = order, probability = prob).save()
        return HttpResponseRedirect(reverse('projects:status'))


class ProjectSimpleCreateView(View):
    def get(self,request):
        context = {
            'clients': Client.objects.filter(is_active=True).all(),
            'statuses': Status.objects.order_by('order').all(),
        }
        return render(request,'projects/project_create_simple.html',context=context)

    def post(self,request):
        p = request.POST
        user = self.request.user
        client = Client.objects.filter(pk=int(p['client'][0])).first()
        contacts = [ClientContact.objects.filter(pk=int(c)).first() for c in p.getlist('contact_person')]
        title = p['title'][0]
        desc = p['description'][0]
        status = Status.objects.filter(pk=int(p['status'][0])).first()
        del_add = p['delivary_address'][0]
        project = Project(
            client = client,
            user = user,
            title = title,
            description = desc,
            status = status,
            delivary_address = del_add
        )
        
        project.save()
        for contact in contacts:
            project.contact_person.add(contact)
        for k in p.keys():
            if 'product_name_' in k:
                product = Product(
                    name = p[k][0],
                    quantity = p['product_qty_'+k[13:]][0],
                    description = p['product_description_'+k[13:]][0],
                    project = project
                ).save()
        return HttpResponseRedirect(project.get_absolute_url)

class StatusDeleteView(DeleteView):
    model = Status
    def get_success_url(self):  
        return reverse('projects:status')
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)
    def form_valid(self, form):
        form.save()
        return reverse('projects:status')


class ProjectListView(ListView):
    model = Project
    template_name = 'projects/projects_list.html'

class ProjectDetailView(DetailView):
    model = Project
    template_name = 'projects/project_detail.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['fileForm'] = FileUploadForm()
        materials = {}
        for purchase in self.object.purchase_set.all():
            for m in purchase.materialqty_set.all():
                materials[m.material.name] = m.quantity
        
        for transfer in self.object.materialtransfer_set.all():
            for m in transfer.materialqtytransfer_set.all():
                if m.material.name not in materials:
                    materials[m.material.name] = 0
                materials[m.material.name] += m.quantity
        
        for rt in self.object.materialreturn_set.all():
            if rt.inventory.material.name not in materials:
                materials[rt.inventory.material.name] = 0
            materials[rt.inventory.material.name] -= rt.quantity

        context['materials'] = materials
        return context



class ProjectSimpleUpdateView(View):
    def get(self,request,pk):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        contacts = {}
        for c in project.company_contacts:
            contacts[c.id] = [c,False]
        for c in project.selected_contacts:
            if c.id in contacts:
                contacts[c.id][1] = True 
        context = {
            'project': project,
            'contacts': contacts
        }
        return render(request,'projects/project_update_simple.html',context=context)
    
    def post(self,request,pk):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        p = request.POST
        user = request.user
        notes = ''
        if p['title'] != project.title:
            notes += f'updated title from "{project.title}" to "{p["title"]}" # '
            Project.objects.filter(pk=project.id).update(title=p['title'])
        if p['description'] != project.description:
            notes += f'updated description from "{project.description}" to "{p["description"]}" # '
            Project.objects.filter(pk=project.id).update(description=p['description'])
        if p['delivery_address'] != project.delivery_address:
            notes += f'updated delivery address from "{project.delivery_address}" to "{p["delivery_address"]}" # '
            Project.objects.filter(pk=project.id).update(delivery_address=p['delivery_address'])
        # Record contacts change
        contacts = {}
        for c in project.company_contacts:
            contacts[c.id] = [c,False]
        for c in project.selected_contacts:
            if c.id in contacts:
                if f'contact_{c.id}' not in p.keys():
                    notes += f'removed contact {c.name} # '
                    project.contact_person.remove(c)
                contacts[c.id][1] = True 
        for k in p.keys():
            if 'contact_' in k:
                c = ClientContact.objects.get(pk=k[8:])
                if not contacts[c.id][1]:
                    notes += f'added contact {c.name} # '
                    project.contact_person.add(c)
        # record product changes
        for k in p.keys():
            if ('product_name_' in k):
                if isnum(k[13:]):
                    prod = Product.objects.get(pk=k[13:])
                    if 'delete_'+k[13:] in p.keys():
                        notes += f"deleted product {prod.id}-{prod.name} # "
                        prod.delete()
                    else:
                        changed = False
                        if (p[k] != prod.name):
                            changed = True
                            notes += f"changed name for product {prod.id}-{prod.name} to {p[k]} # "
                            Product.objects.filter(pk=k[13:]).update(name=p[k])
                        if p['product_qty_'+k[13:]] != prod.quantity:
                            changed = True
                            notes += f"changed quantity for product {prod.id}-{prod.name} to {p['product_qty_'+k[13:]]} # "
                            Product.objects.filter(pk=k[13:]).update(quantity=p['product_qty_'+k[13:]])
                        if p['product_description_'+k[13:]] != prod.description:
                            changed = True
                            notes += f"changed product description for product {prod.id}-{prod.name} to {p['product_description_'+k[13:]]} # "
                            Product.objects.filter(pk=k[13:]).update(description=p['product_description_'+k[13:]])
                else:
                    notes += f"new product name = '{p[k]}', qty = '{p['product_qty_'+k[13:]]}' and description = '{p['product_description_'+k[13:]]}' is created. # "
                    Product(
                        project = project,
                        name = p[k],
                        quantity = p['product_qty_'+k[13:]],
                        description = p['product_description_'+k[13:]]
                    ).save()
        ProjectTimeline(
            project = project,
            notes = notes,
            status = project.status,
            user = user
        ).save()
        return HttpResponseRedirect(project.get_absolute_url)


class ProjectUpdateView(UpdateView):
    model = Project
    template_name = 'projects/project_update.html'
    fields = ['title','description','status','delivary_address']

    
    def get_success_url(self):
        # return self.success_url
        return self.get_object().get_absolute_url

    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['all_contacts'] = self.object.company_contacts
        context['current_contacts'] = self.object.selected_contacts
        context['client'] = self.get_object().client
        context['update']= True
        contacts = [ i.id for i in self.get_object().contact_person.all() ]
        context['current_contacts'] = contacts
        return context
    
    def form_valid(self, form):
        user = self.request.user
        for f in form:
            print(f.name,f.data)
        object = self.get_object()
        notes = ""
        # Create notes based on what is changed
        for f in form:
            if f.name in form.changed_data:
                if f.name == 'contact_person':
                    
                    new_contact = ClientContact.objects.get_first(f.data)
                    notes += f" {f.name} = {new_contact.name}."
                elif f.name == 'status':
                    new_status = Status.objects.get_first(f.data)
                    notes += f" {f.name} = {new_status.status}."
                else:
                    notes += f" {f.name} = {f.data}."
        # if there are updated then log the timeline
        if len(notes) > 0:
            notes = f"Updates: " + notes
            ProjectTimeline(project=object,status=self.get_object().status,notes = notes,user = user).save()
        return super().form_valid(form)

class ProjectPopView(CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    fields = ['title','description','status','delivary_address']


class ProjectCreateView(CreateView):
    model = Project
    # form_class = ProjectForm
    template_name = 'projects/project_create.html'
    fields = ['client','contact_person','title','description','status','delivary_address']

    def get_success_url(self):
        return self.object.get_absolute_url

    def form_valid(self, form):
        user = self.request.user
        for f in form:
            print(f.name,f.data)
        self.object = form.save()
        status = ""
        notes = "Initiated project with: "
        # Create notes based on what is changed
        for f in form:
            if f.name == 'contact_person':
                for c in set(f.data):
                    new_contact = ClientContact.objects.get_first(c)
                    notes += f" {f.name} =  {new_contact.name}."
            elif f.name == 'status':
                new_status = Status.objects.get_first(f.data)
                notes += f" {f.name} = {new_status.status}."
                status = new_status
            else:
                notes += f" {f.name} = {f.data}."
        print(notes)
        self.update = ProjectTimeline(project=self.object,status=status,notes = notes,user = user).save()
        return super().form_valid(form)



class ProjectDeleteView(DeleteView):
    model = Project

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
    
    def get(self, request, *args, **kwargs):
        return self.delete(request, *args, **kwargs)


class ProjectFileDeleteView(DeleteView):
    model = ProjectFiles
    project = None

    def get_success_url(self):
        return self.project.get_absolute_url

    def get(self, request, *args, **kwargs):
        user = request.user
        object = self.get_object()
        self.project = object.project
        notes = "Deleted file " + object.get_file_name()
        ProjectTimeline(project=self.project,status=self.project.status,notes = notes,user = user).save()
        return self.delete(request, *args, **kwargs)


@xframe_options_exempt
def handle_upload_file(request):
    f = request.FILES['file']
    user = request.user
    project_id = request.POST['project_id']
    notes = request.POST['notes']
    project = Project.objects.get_first(project_id)
    pf = ProjectFiles(project=project
                    ,file=f
                    ,notes=notes)
    pf.save()
    ProjectTimeline(project=project
                    ,status=project.status
                    ,notes = f'Uploaded: {pf.get_file_name()} ## {notes}'
                    ,project_file = pf
                    ,user = user).save()
    return HttpResponseRedirect(project.get_absolute_url)

class KanbanBoard(View):
    def get(self,request):
        context = {
            'statuses': Status.objects.order_by('order').all()
        }
        return render(request,'projects/kanbanboard.html',context=context)


class MaterialReturnView(View):
    def get(self,request, pk):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        materials = {}
        for purchase in project.purchase_set.all():
            for m in purchase.materialqty_set.all():
                materials[m.material.name] = [m.material,m.quantity]
        
        for transfer in project.materialtransfer_set.all():
            for m in transfer.materialqtytransfer_set.all():
                if m.material.name not in materials:
                    materials[m.material.name] = [m.material,0]
                materials[m.material.name][1] += m.quantity
        
        for rt in project.materialreturn_set.all():
            if rt.inventory.material.name not in materials:
                materials[rt.inventory.material.name] = [rt.inventory.material,0]
            materials[rt.inventory.material.name][1] -= rt.quantity

        context = {
            'project': project,
            'materials': materials,
            'warehouses': Warehouse.objects.all()
        }
        return render(request,'projects/return_create_simple.html',context)
    def post(self,request,pk):
        p = request.POST
        user = request.user
        project = Project.objects.filter(pk=p['project']).first()
        dt = p['date']
        returns = []
        notes = 'Returned:: '
        for k in p.keys():
            if 'material_' in k:
                m = Material.objects.filter(pk=k[9:]).first()
                q = float(p['ret_quantity_'+k[9:]])
                w = p['warehouse_'+k[9:]]
                if (q > 0) and len(w) > 0:
                    returns.append([m,q,w])
                    warehouse = Warehouse.objects.filter(pk=w).first()
                    inventory, created = Inventory.objects.get_or_create(material=m,warehouse=warehouse)
                    print('Inventory: ', inventory, created)
                    notes += f'{m.name} qty: {q} --> {warehouse}, '
                    mr = MaterialReturn(
                        date=dt,
                        project = project,
                        inventory = inventory,
                        quantity = q,
                        user = user
                    )
                    mr.save()
                    inventory.quantity += q
                    inventory.save()
        print(returns)
        pt = ProjectTimeline(project=project,status=project.status,notes = notes,user = user).save()
        return HttpResponseRedirect(project.get_absolute_url)
    


class DeliveryChallanCreateView(View):
    def get(self,request,pk):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        products = {}
        for product in project.product_set.all():
            products[f'{product.id}'] = [product,product.quantity]
        
        for dc in project.deliverychallan_set.all():
            for dp in dc.deliveryproduct_set.all():
                print(dp.product.id)
                if f'{dp.product.id}' in products:
                    products[f'{dp.product.id}'][1] -= dp.quantity
        
        for p in products.keys():
            if products[p][1] == 0:
                products.pop(p)
        
        
        context = {
            'products': products,
            'project': project,
        }
        return render(request,'projects/delivery_challan_simple.html',context=context)
    def post(self,request,pk):
        p = request.POST
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        dt = p['date']
        cn = p['challan_no']
        address = p['address']
        user = request.user
        dc = DeliveryChallan(
            project = project,
            date = dt,
            challanNo = cn,
            address = address,
            user = user
        )
        dc.save()
        products = []
        for k in p.keys():
            if 'product_' in k:
                products.append(k[8:])
                product = Product.objects.filter(pk=k[8:]).first()
                qty = p['send_quantity_'+k[8:]]
                DeliveryProduct(
                    deliveryChallan = dc,
                    product = product,
                    quantity = qty
                ).save()
        
        return self.get(request,pk)

def changeStatus(self,request):
    project = request.POST['project_id']
    status = request.POST['status']

    return ''
