from django.shortcuts import render, HttpResponseRedirect
from django.views.generic import ListView, CreateView, DetailView, UpdateView, DeleteView
from .models import Client, ClientContact
from django.urls import reverse

# Create your views here.


class ClientListView(ListView):
    model = Client
    template_name = 'clients/clients_list.html'


class ClientDetailView(DetailView):
    model = Client
    template_name = 'clients/client_detail.html'
    

class ClientCreateView(CreateView):
    model = Client
    template_name = 'clients/client_create.html'
    fields = '__all__'


class ClientUpdateView(UpdateView):
    model = Client
    fields = '__all__'
    template_name = 'clients/client_create.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['update']= True
        return context
    


class ClientContactAddView(CreateView):
    model = ClientContact
    template_name = 'clients/client_contact_create.html'
    fields = ['name','contact_number','designation']
    
    def get_success_url(self):
        return reverse('clients:client_detail', kwargs={'pk': self.kwargs.get('pk')})

        
    def form_valid(self, form):
        form.instance.client_id = self.kwargs.get('pk')
        form.save()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())


class ClientContactUpdateView(UpdateView):
    model = ClientContact
    template_name = 'clients/client_contact_create.html'
    fields = ['name','contact_number','designation']
    
    def get_success_url(self):
        return reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        
        context['update']= True
        return context


    def form_valid(self, form):
        form.instance.client_id = self.get_object().client.pk
        form.save()
        super().form_valid(form)
        return HttpResponseRedirect(self.get_success_url())

class ClientContactDeleteView(DeleteView):
    model = ClientContact

    def get_success_url(self):  
        return self.su

    
    def get(self, request, *args, **kwargs):
        self.su = reverse('clients:client_detail', kwargs={'pk': self.get_object().client.pk})
        return self.delete(request, *args, **kwargs)

    def form_valid(self, form):
        form.save()
        return HttpResponseRedirect(self.su)
    
def load_client_contact(request):
    client_id = int(request.GET.get('client'))
    print(request.GET.getlist('current_contacts'))
    if 'current_contacts' in request.GET:
        current_contacts = [ int(i) for i in request.GET.getlist('current_contacts')]
    else:
        current_contacts = []
    client_contacts = ClientContact.objects.filter(client_id=client_id).order_by('name')
    return render(request, 'clients/contact_dropdown_list_options.html', {
        'client_contacts': client_contacts,
        'current_contacts': current_contacts})