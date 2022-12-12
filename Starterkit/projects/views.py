from django.shortcuts import render, HttpResponseRedirect, HttpResponse
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView, View
from django.views.generic.edit import FormView
from .models import *
from clients.models import *
from .forms import ProjectForm, FileUploadForm, ProductFormSet
from django.urls import reverse
from django.views.decorators.clickjacking import xframe_options_exempt


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
        return context


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
    fields = '__all__'


class ProjectCreateView(CreateView):
    model = Project
    # form_class = ProjectForm
    template_name = 'projects/project_create.html'
    fields = '__all__'

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


def changeStatus(self,request):
    project = request.POST['project_id']
    status = request.POST['status']

    return ''
