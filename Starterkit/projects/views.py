from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import *
from clients.models import *
from .forms import ProjectForm, FileUploadForm, ProductFormSet
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt
from materials.models import Warehouse, Material, Inventory, MaterialReturn
from datetime import datetime
from xhtml2pdf import pisa
from django.template.loader import get_template
from io import BytesIO
from settings.models import AppSettings
from django.conf import settings

def render_to_pdf(template_src, context_dict={}):
	template = get_template(template_src)
	html  = template.render(context_dict)
	result = BytesIO()
	pdf = pisa.pisaDocument(BytesIO(html.encode("ISO-8859-1")), result)
	if not pdf.err:
		return HttpResponse(result.getvalue(), content_type='application/pdf')
	return None



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
            'clients': Client.objects.filter(is_active=True).filter(is_customer=True).all(),
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
        project = self.get_object()
        products = {}
        for product in project.product_set.all():
            products[f'{product.id}'] = [product,product.quantity,0,0,product.quantity] # product, quantity, delivered, returned, remaining 
        for dc in project.deliverychallan_set.all():
            for dp in dc.deliveryproduct_set.all():
                if f'{dp.product.id}' in products.keys():
                    products[f'{dp.product.id}'][2] += dp.quantity
                    products[f'{dp.product.id}'][4] -= dp.quantity
        for ret in project.returns_set.all():
            for pr in ret.productreturn_set.all():
                if f'{pr.product.id}' in products.keys():
                    products[f'{pr.product.id}'][3] += pr.quantity
                    products[f'{pr.product.id}'][4] += pr.quantity
        context['products'] = products
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
            type = 'project',
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
            ProjectTimeline(project=object,status=self.get_object().status,type='project',notes = notes,user = user).save()
        return super().form_valid(form)

class ProjectPopView(CreateView):
    model = Project
    template_name = 'projects/project_create.html'
    fields = ['title','description','status','delivary_address']


# class ProjectCreateView(CreateView):
#     model = Project
#     # form_class = ProjectForm
#     template_name = 'projects/project_create.html'
#     fields = ['client','contact_person','title','description','status','delivary_address']

#     def get_success_url(self):
#         return self.object.get_absolute_url

#     def form_valid(self, form):
#         user = self.request.user
#         for f in form:
#             print(f.name,f.data)
#         self.object = form.save()
#         status = ""
#         notes = "Initiated project with: "
#         # Create notes based on what is changed
#         for f in form:
#             if f.name == 'contact_person':
#                 for c in set(f.data):
#                     new_contact = ClientContact.objects.get_first(c)
#                     notes += f" {f.name} =  {new_contact.name}."
#             elif f.name == 'status':
#                 new_status = Status.objects.get_first(f.data)
#                 notes += f" {f.name} = {new_status.status}."
#                 status = new_status
#             else:
#                 notes += f" {f.name} = {f.data}."
#         print(notes)
#         self.update = ProjectTimeline(project=self.object,status=status,type='project',notes = notes,user = user).save()
#         return super().form_valid(form)



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
        ProjectTimeline(project=self.project,status=self.project.status,type='file',notes = notes,user = user).save()
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
        ProjectTimeline(project=project,status=project.status,type='material',notes = notes,user = user).save()
        return HttpResponseRedirect(project.get_absolute_url)
    
class DeliveryChallanUpdateView(View):
    def get(self,request,pk,dc_id,message=""):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        challan = DeliveryChallan.objects.filter(pk=self.kwargs['dc_id']).first()
        print(challan.date,type(challan.date))
        products = {}
        for product in project.product_set.all():
            products[f'{product.id}'] = [product,product.quantity,0]
        
        for dc in project.deliverychallan_set.all():
            if dc.id != challan.id:
                for dp in dc.deliveryproduct_set.all():
                    if f'{dp.product.id}' in products:
                        products[f'{dp.product.id}'][1] -= dp.quantity
            else:
                for dp in dc.deliveryproduct_set.all():
                    if f'{dp.product.id}' in products:
                        products[f'{dp.product.id}'][2] = dp.quantity
        
        for p in products.keys():
            if products[p][1] == 0:
                products.pop(p)
        
        
        context = {
            'products': products,
            'project': project,
            'challan': challan,
            'message': message,
            'date': challan.date.strftime("%Y-%m-%d")
        }
        return render(request,'projects/delivery_challan_update_simple.html',context=context)
        
    def post(self,request,pk,dc_id):
        p = request.POST
        project = Project.objects.filter(pk=pk).first()
        dc = DeliveryChallan.objects.filter(pk=dc_id).first()
        sending = False
        print(p)
        for k in p.keys():
            if 'send_quantity_' in k:
                if float(p[k]) > 0:
                    sending = True
        if not sending:
            print('Not sending')
            return self.get(request,pk,'Choose at least one product to send')
        dc.date = p['date']
        dc.challanNo = p['challan_no']
        dc.address = p['address']
        dc.vehicleNo = p['vehicle_no']
        dc.user = request.user
        dc.save()
        products = []
        for k in p.keys():
            if 'product_' in k:
                products.append(k[8:])
                product = Product.objects.filter(pk=k[8:]).first()
                qty = float(p['send_quantity_'+k[8:]])
                pr, _ = DeliveryProduct.objects.get_or_create(
                    deliveryChallan = dc,
                    product = product,
                    
                )
                print(pr)
                pr.quantity = qty
                pr.save()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'product',
                user = request.user,
                notes = f"Delivery <a href='{dc.get_absolute_url}'>challan</a> updated"
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)

class DeliveryChallanPDFView(View):
    def get(self,request,pk,dc_id):
        project = Project.objects.filter(pk=pk).first()
        challan = DeliveryChallan.objects.get(pk=dc_id)
        appsettings,_ = AppSettings.objects.get_or_create()
        context = {
            'challan': challan,
            'app_settings': appsettings,
        }
        pdf = render_to_pdf('projects/pdf_template.html',context)
        return HttpResponse(pdf, content_type='application/pdf')
        # return render(request,'projects/pdf_template.html',context)

class DeliveryReturnCreateView(View):
    def get(self,request,pk,dc_id,message=""):
        project = Project.objects.filter(pk=pk).first()
        challan = DeliveryChallan.objects.get(pk=dc_id)
        products = {}
        for p in challan.deliveryproduct_set.all():
            products[f"{p.product.id}"] = [p.product, p.quantity]
        for dr in challan.returns_set.all():
            for p in dr.productreturn_set.all():
                if f"{p.product.id}" in products:
                    products[f"{p.product.id}"][1] -= p.quantity
            
        context = {
            'project': project,
            'challan': challan,
            'products': products,
            'message': message,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        return render(request,'projects/productreturn_simple_create.html',context)
    def post(self,request,pk,dc_id):
        project = Project.objects.filter(pk=pk).first()
        challan = DeliveryChallan.objects.get(pk=dc_id)
        p = request.POST
        print(p)
        returning = False
        returns = []
        for k in p.keys():
            if 'return_quantity_' in k:
                if float(p[k]) > 0:
                    returns.append([k[16:],p[k]])
                    returning = True
        if not returning:
            return self.get(request,pk,dc_id,'Choose at least one product to return')
        products = {}
        for pr in challan.deliveryproduct_set.all():
            products[f"{pr.product.id}"] = [pr.product, pr.quantity]
        for dr in challan.returns_set.all():
            for pr in dr.productreturn_set.all():
                if f"{pr.product.id}" in products:
                    products[f"{pr.product.id}"][1] -= pr.quantity
        pr = Returns(
            project = project,
            date = p['date'],
            challan = challan,
            user = request.user
        )
        pr.save()
        for pk, qty in returns:
            ProductReturn(
                return_id = pr,
                product = products[pk][0],
                notes = p[f"notes_{pk}"],
                quantity = min(float(qty),float(products[pk][1]))
            ).save()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'product',
                user = request.user,
                notes = f"Products returned from <a href='{challan.get_absolute_url}'>{challan.challanNo}</a>."
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)


class DeliveryChallanDeleteView(DeleteView):
    model = DeliveryChallan

    def get_success_url(self):
        return self.request.META.get('HTTP_REFERER')
    
    def get(self, request, *args, **kwargs):
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'product',
                user = request.user,
                notes = f"Deleted delivery challan {self.get_object().challanNo}."
            ).save()
        return self.delete(request, *args, **kwargs)        


class DeliveryChallanCreateView(View):
    def get(self,request,pk,message=""):
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        products = {}
        for product in project.product_set.all():
            products[f'{product.id}'] = [product,product.quantity]
        
        for dc in project.deliverychallan_set.all():
            for dp in dc.deliveryproduct_set.all():
                if f'{dp.product.id}' in products:
                    products[f'{dp.product.id}'][1] -= dp.quantity
        for ret in project.returns_set.all():
            for pr in ret.productreturn_set.all():
                if f'{pr.product.id}' in products:
                    products[f'{pr.product.id}'][1] += pr.quantity
                    
        for p in products.keys():
            if products[p][1] == 0:
                products.pop(p)
        
        
        context = {
            'products': products,
            'project': project,
            'message': message
        }
        return render(request,'projects/delivery_challan_simple.html',context=context)
    def post(self,request,pk):
        p = request.POST
        print(p)
        project = Project.objects.filter(pk=self.kwargs['pk']).first()
        sending = False
        for k in p.keys():
            if 'send_quantity_' in k:
                if float(p[k]) > 0:
                    sending = True
        if not sending:
            return self.get(request,pk,'Choose at least one product to send')
        dt = p['date']
        cn = p['challan_no']
        address = p['address']
        vehicle_no = p['vehicle_no']
        user = request.user
        dc = DeliveryChallan(
            project = project,
            date = dt,
            challanNo = cn,
            vehicleNo = vehicle_no,
            address = address,
            user = user
        )
        dc.save()
        products = []
        for k in p.keys():
            if 'product_' in k:
                products.append(k[8:])
                product = Product.objects.filter(pk=k[8:]).first()
                qty = float(p['send_quantity_'+k[8:]])
                DeliveryProduct(
                    deliveryChallan = dc,
                    product = product,
                    quantity = qty
                ).save()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'product',
                user = request.user,
                notes = f"Created delivery <a href='{dc.get_absolute_url}'>challan</a>."
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)


class InwardMaterialCreateView(View):
    def get(self,request,pk,message=""):
        project = Project.objects.get(pk=pk)
        context = {
            'project': project,
            'date': datetime.now().strftime("%Y-%m-%d")
        }
        return render(request,'projects/inward_simple_create.html',context)
    def post(self,request,pk):
        p = request.POST
        print(p)
        getting = False
        for k in p.keys():
            if 'imaterial_qty_' in k:
                if float(p[k]) > 0:
                    getting = True
        if not getting:
            return self.get(request,pk,"Add at least one inward material")
        project = Project.objects.get(pk=pk)
        dt = p['date']
        challan = p['challan']
        imchallan = IMChallan(
            date = dt,
            challanNo = challan,
            user = request.user,
            project = project
        )
        imchallan.save()
        for k in p.keys():
            if 'imaterial_qty_' in k:
                imaterial = p['imaterial_'+k[14:]]
                quantity = p[k]
                IMQty(
                    imaterial = imaterial,
                    quantity = quantity,
                    imchallan = imchallan
                ).save()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'material',
                user = request.user,
                notes = f"Inward material: <a href='{imchallan.get_absolute_url}'>Challan: {challan}</a>."
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)


class InwardMaterialUpdateView(View):
    def get(self,request,pk,imc,message=""):
        project = Project.objects.get(pk=pk)
        imchallan = IMChallan.objects.get(pk=imc)
        context = {
            'project': project,
            'imchallan': imchallan,
            'date': imchallan.date.strftime("%Y-%m-%d")
        }
        return render(request,'projects/inward_simple_update.html',context)
    def post(self,request,pk,imc):
        p = request.POST
        getting = False
        for k in p.keys():
            if 'imaterial_qty_' in k:
                if float(p[k]) > 0:
                    getting = True
        if not getting:
            return self.get(request,pk,"Add at least one inward material")
        project = Project.objects.get(pk=pk)
        imchallan = IMChallan.objects.get(pk=imc)
        dt = p['date']
        challan = p['challan']
        imchallan.date = dt
        imchallan.challanNo = challan
        imchallan.save()
        for k in p.keys():
            if 'imaterial_qty_' in k:
                try:
                    imaterial = IMQty.objects.filter(pk=k[14:]).first()
                except:
                    imaterial = IMQty(
                        imaterial = '',
                        quantity = 0,
                        imchallan = imchallan
                    )
                imaterial.imaterial = p['imaterial_'+k[14:]]
                imaterial.quantity = p[k]
                imaterial.save()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'material',
                user = request.user,
                notes = f"Updated Inward material: <a href='{imchallan.get_absolute_url}'>Challan: {challan}</a>."
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)

class InwardMaterialDeleteView(View):
    def get(self,request,pk,imc):
        project = Project.objects.get(pk=pk)
        imchallan = IMChallan.objects.get(pk=imc)
        for imaterial in imchallan.imqty_set.all():
            imaterial.delete()
        imchallan.delete()
        ProjectTimeline(
                project = project,
                status = project.status,
                type = 'material',
                user = request.user,
                notes = f"Deleted Inward material Challan: {imchallan.challan}."
            ).save()
        return HttpResponseRedirect(project.get_absolute_url)

@xframe_options_exempt
def changeStatus(request):
    project = Project.objects.get(pk=request.POST['project_id'])
    status = Status.objects.get(pk=request.POST['status'][7:])
    sibling_id = int(request.POST['sibling'])
    new_rank = None
    if sibling_id > 0:
        new_rank = Project.objects.get(pk=sibling_id).status_rank
    print(project,status,sibling_id,new_rank)
    
    ProjectTimeline(
        project = project,
        status = project.status,
        type = 'project',
        user = request.user,
        notes = f"Changed status from {project.status.status} to {status.status}"
    ).save()
    project.change_status(status,request.user)
    project.change_status_rank(new_rank)
    return ''
